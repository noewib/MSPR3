# Documentation Technique & Runbook d'Exploitation
## Solution IA de Prédiction de Consommation Électrique Nationale — EDF / RTE
### MSPR TPRE932 & TPRE942 — CDPIA 2025-2026

---

> [!IMPORTANT]
> Ce document constitue le livrable 2 officiel : Documentation Technique & Runbook d'Exploitation. Il doit être lu conjointement avec le **Livrable 1 — Dossier de Déploiement & de Maintenabilité** pour une vision complète de l'opération du système.

---

## Table des Matières

1. [Documentation Technique](#1-documentation-technique)
   - 1.1 Vue d'ensemble de l'architecture logicielle
   - 1.2 Description des modèles ML
   - 1.3 Pipeline de données — `DataPipeline`
   - 1.4 Services de déploiement
   - 1.5 Pipeline CI/CD — GitHub Actions
   - 1.6 Prérequis techniques
2. [Runbook d'Exploitation](#2-runbook-dexploitation)
   - 2.1 Démarrer la solution
   - 2.2 Arrêter la solution
   - 2.3 Déployer une nouvelle version de modèle
   - 2.4 Rollback d'urgence
   - 2.5 Checks essentiels — Vérifier que tout fonctionne
3. [Gestion des Incidents](#3-gestion-des-incidents)
   - 3.1 Incident A : Chute de performances du modèle
   - 3.2 Incident B : Service ne répond plus (API muette)
   - 3.3 Incident C : Dérive de données détectée
   - 3.4 Incident D : Changement de format des données entrantes
   - 3.5 Incident E : Mémoire insuffisante (OOMKilled)
4. [Références Croisées — Livrable 1](#4-références-croisées--livrable-1)
5. [Note d'Expertise Technique à l'Équipe Projet](#5-note-dexpertise-technique-à-léquipe-projet)

---

## 1. Documentation Technique

### 1.1 Vue d'Ensemble de l'Architecture Logicielle

```
c:\Users\USER\Documents\MSPR\
│
├── src/
│   ├── api/
│   │   └── app.py                  ← API FastAPI (endpoints, Prometheus, chargement modèle)
│   ├── data/
│   │   └── data_pipeline.py        ← Ingestion, feature engineering, normalisation
│   ├── models/
│   │   ├── train_evaluate.py       ← Entraînement, évaluation comparative, logs MLflow
│   │   └── custom_rbfn.py          ← Implémentation RBFN personnalisée (KMeans + Ridge)
│   ├── monitoring/
│   │   └── drift_detector.py       ← Détection de dérive KS-test + Evidently AI
│   └── pipelines/
│       └── retraining_dag.py       ← DAG Airflow : extract → train → evaluate
│
├── models/                         ← Artefacts sérialisés en production
│   ├── best_model.joblib           ← Modèle champion actif (KNeighbors)
│   ├── data_pipeline.joblib        ← Pipeline avec StandardScaler ajusté
│   ├── mlflow_logs.json            ← Métriques de tous les entraînements
│   └── drift_report.json           ← Dernier rapport de dérive
│
├── k8s/
│   ├── deployment.yaml             ← Déploiement K8s (3 répliques, RollingUpdate)
│   ├── service.yaml                ← Service LoadBalancer (port 80 → 8000)
│   └── hpa.yaml                    ← HPA (3–10 pods, seuil CPU 70%)
│
├── tests/
│   ├── test_api.py                 ← Tests d'intégration API (5 cas)
│   ├── test_data_pipeline.py       ← Tests unitaires pipeline (3 cas)
│   └── test_custom_rbfn.py         ← Tests unitaires RBFN (2 cas)
│
├── locust/
│   └── locustfile.py               ← Tests de charge (10–200 users virtuels)
│
├── .github/workflows/
│   └── ci_cd.yml                   ← Pipeline CI/CD (lint → test → scan → build)
│
├── Dockerfile                      ← Construction multi-stage (builder + runner)
└── requirements.txt                ← Dépendances Python versionnées
```

---

### 1.2 Description des Modèles ML

#### Modèle 1 — K-Nearest Neighbors (KNeighbors) ⭐ Champion de Production

| Attribut | Valeur |
|:---|:---|
| **Classe** | `sklearn.neighbors.KNeighborsRegressor` |
| **Fichier** | `src/models/train_evaluate.py` (ligne 55) |
| **Artefact** | `models/best_model.joblib` |
| **Statut** | **Champion — En production** |

**Hyperparamètres de production :**
```python
KNeighborsRegressor(
    n_neighbors = 5,        # Nombre de voisins considérés
    weights     = 'distance' # Pondération inverse de la distance (voisins proches = plus influents)
)
```

**Variables d'entrée (après prétraitement) :**

| Variable | Type | Description | Plage typique |
|:---|:---:|:---|:---:|
| `temperature` | float | Température nationale moyenne (°C) | -5 à 40°C |
| `hour_sin` | float | Encodage cyclique sinus de l'heure | [-1.0, 1.0] |
| `hour_cos` | float | Encodage cyclique cosinus de l'heure | [-1.0, 1.0] |
| `month_sin` | float | Encodage cyclique sinus du mois | [-1.0, 1.0] |
| `month_cos` | float | Encodage cyclique cosinus du mois | [-1.0, 1.0] |
| `day_of_week` | int | Jour de la semaine (0=lundi, 6=dimanche) | [0, 6] |
| `is_weekend` | int | Indicateur binaire week-end | {0, 1} |
| `is_holiday` | int | Indicateur binaire jour férié France | {0, 1} |
| `lag_24h` | float | Consommation à t-24h (MW) | 35 000 – 95 000 MW |
| `lag_48h` | float | Consommation à t-48h (MW) | 35 000 – 95 000 MW |
| `lag_7d` | float | Consommation à t-7 jours (MW) | 35 000 – 95 000 MW |
| `temp_roll_mean_3h` | float | Moyenne glissante température 3h | -5 à 40°C |
| `temp_roll_mean_6h` | float | Moyenne glissante température 6h | -5 à 40°C |

**Prétraitements appliqués :**
1. Feature engineering complet (lags, encodages cycliques, indicateurs calendaires) via `DataPipeline.feature_engineering()`
2. Normalisation `StandardScaler` (moyenne = 0, écart-type = 1) ajusté sur train, appliqué sur test/prod

**Sortie :**
- `prediction_mw` : Consommation électrique nationale prédite en **mégawatts (MW)**

**Métriques de performance (180j historique, split 80/20 chronologique) :**
```
R²      : 0.6011   (variance expliquée par le modèle)
RMSE    : 3 142 MW (erreur absolue quadratique moyenne)
MAPE    : 4.68%    (erreur relative moyenne — en dessous du seuil critique de 5%)
Acc ±5% : 69.48%   (fraction de prédictions dans les ±5% de tolérance métier)
Latence : < 1 ms   (inférence CPU mono-thread, quasi-instantanée)
```

**Pourquoi KNN a été sélectionné :**
- Meilleur MAPE parmi les 4 modèles (4,68% vs 4,87% RandomForest)
- Temps d'entraînement le plus court (0,009 s)
- Latence d'inférence négligeable (< 1 ms), compatible contrainte temps réel
- Pas d'hyperparamètres complexes à tuner, bon comportement naturel sur séries temporelles avec lags

---

#### Modèle 2 — Random Forest Regressor

| Attribut | Valeur |
|:---|:---|
| **Classe** | `sklearn.ensemble.RandomForestRegressor` |
| **Fichier** | `src/models/train_evaluate.py` (ligne 54) |
| **Statut** | Challenger principal (ré-entraînement Airflow) |

**Hyperparamètres :**
```python
RandomForestRegressor(
    n_estimators = 30,      # 30 arbres de décision (compromis vitesse/précision)
    max_depth    = 10,      # Profondeur max pour éviter le surapprentissage
    random_state = 42,      # Reproductibilité
    n_jobs       = -1       # Parallélisation sur tous les cœurs CPU
)
```
*(Configuration enrichie dans le DAG de ré-entraînement : `n_estimators=40, max_depth=12`)*

**Variables d'entrée :** Identiques au KNeighbors (13 variables après feature engineering + normalisation).

**Métriques :**
```
R²      : 0.5838
RMSE    : 3 209 MW
MAPE    : 4.87%
Acc ±5% : 67.97%
Train   : 0.064 s
```

**Forces :**
- Robuste au bruit et aux valeurs aberrantes (agrégation de 30 arbres)
- Sortie des importances de features via `feature_importances_` (utilisable avec SHAP)
- Gestion native des relations non-linéaires complexes

**Faiblesses vs KNN :**
- MAPE légèrement plus élevé (4,87% vs 4,68%)
- Temps d'entraînement x7 plus lent (0,064 s vs 0,009 s)
- Taille du modèle serialisé plus importante (forêt de 30 arbres)

---

#### Modèle 3 — Decision Tree Regressor

| Attribut | Valeur |
|:---|:---|
| **Classe** | `sklearn.tree.DecisionTreeRegressor` |
| **Fichier** | `src/models/train_evaluate.py` (ligne 53) |
| **Statut** | Référence de base (baseline) |

**Hyperparamètres :**
```python
DecisionTreeRegressor(
    max_depth    = 8,       # Limitation de la profondeur pour éviter l'overfitting
    random_state = 42
)
```

**Métriques :**
```
R²      : 0.4712
RMSE    : 3 618 MW
MAPE    : 5.48%    ← DÉPASSE le seuil métier critique de 5%
Acc ±5% : 64.42%
Train   : 0.020 s
```

**Usage :** Modèle de référence simple pour évaluer le gain des modèles plus complexes. Son MAPE de 5,48% le disqualifie pour la production directe mais il sert de borne inférieure dans l'évaluation Champion/Challenger.

**Interprétabilité :** Arbre visualisable via `sklearn.tree.export_text()`, utile pour les explications métier et l'auditabilité réglementaire.

---

#### Modèle 4 — RBFN (Réseau de Fonctions à Base Radiale) — Implémentation Custom

| Attribut | Valeur |
|:---|:---|
| **Classe** | `RadialBasisFunctionNetwork` (implémentation maison) |
| **Fichier** | `src/models/custom_rbfn.py` |
| **Statut** | Expérimental — Non retenu pour la production |

**Architecture du modèle :**
```
Entrée (13 features)
    │
    ▼
┌──────────────────────────────────────────────────┐
│  Étape 1 : KMeans (n_clusters=30)                │
│  → Identification de 30 centres dans l'espace    │
│    des features d'entraînement                   │
└──────────────────────────┬───────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────┐
│  Étape 2 : Activations Gaussiennes               │
│  φ(r) = exp(-γ · r²)                             │
│  γ = 1 / (2σ²), σ = distance moyenne entre      │
│  centres (si gamma='scale')                       │
└──────────────────────────┬───────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────┐
│  Étape 3 : Régression Ridge (α=0.1)              │
│  → Apprentissage des poids de sortie             │
│    avec régularisation L2                         │
└──────────────────────────┬───────────────────────┘
                           │
                           ▼
              Sortie : prédiction (MW)
```

**Hyperparamètres :**
```python
RadialBasisFunctionNetwork(
    n_centers    = 30,      # Nombre de fonctions de base (centres KMeans)
    gamma        = 'scale', # Largeur noyau auto-calculée (1/2σ²)
    alpha        = 0.1,     # Régularisation Ridge L2
    random_state = 42
)
```

**Métriques :**
```
R²      : -0.3613  ← NÉGATIF : pire qu'une prédiction par la moyenne
RMSE    : 5 804 MW
MAPE    : 9.19%    ← Inacceptable (quasi-double du seuil critique)
Acc ±5% : 48.04%
Train   : 1.251 s  ← Le plus lent (KMeans + calcul des distances entre centres)
```

> [!WARNING]
> Le RBFN présente un R² négatif sur les données de test, indiquant que le modèle n'a pas convergé correctement sur cet ensemble de données (la moyenne serait une meilleure prédiction). Ce résultat peut s'expliquer par : (1) un nombre insuffisant de centres (30 pour un espace 13D complexe), (2) une mauvaise estimation de γ sur données synthétiques, (3) l'inadéquation des fonctions radiales gaussiennes pour les séries temporelles. Le modèle est conservé à titre pédagogique pour illustrer la diversité des approches.

---

### 1.3 Pipeline de Données — `DataPipeline`

**Fichier :** `src/data/data_pipeline.py`

Le `DataPipeline` est la colonne vertébrale du système. Il est instancié, ajusté (`fit_transform`), et serialisé avec le modèle dans `models/data_pipeline.joblib`.

#### A. Ingestion — `fetch_realtime_data()` et `generate_historical_data()`

```python
# Flux de décision lors de l'ingestion
try:
    # Tentative sur l'API ODRE (Open Data Réseaux Électriques)
    GET https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-national-tr/records
    timeout = 5s
    → Colonnes extraites : date_heure, consommation, temperature (simulée si absente)

except (connexion échouée, timeout, données vides):
    # Fallback : données synthétiques hautes-fidélité
    generate_historical_data(days=3)
```

**Modèle de génération synthétique :**
```
consommation(t) = base_load
                + thermosensibilité(température)  # max(0, 15 - T) × 1 800 MW/°C
                + facteur_journalier(heure)        # deux pics : 8-13h et 18-21h
                + facteur_hebdomadaire(jour)        # -6 000 MW le week-end
                + facteur_jours_fériés             # -6 000 MW les jours fériés
                + bruit_gaussien(σ = 800 MW)
```

#### B. Feature Engineering — `feature_engineering(df, is_training)`

**Variables créées à partir des données brutes :**

```python
# 1. Encodages cycliques (évitent la discontinuité lundi/dimanche, janvier/décembre)
df['hour_sin']   = sin(2π × heure / 24)
df['hour_cos']   = cos(2π × heure / 24)
df['month_sin']  = sin(2π × mois / 12)
df['month_cos']  = cos(2π × mois / 12)

# 2. Indicateurs calendaires
df['day_of_week'] = datetime.dayofweek       # 0 (lun) → 6 (dim)
df['is_weekend']  = 1 si dayofweek >= 5
df['is_holiday']  = 1 si date in holidays.France()

# 3. Lags temporels (données toutes les 30 min → passsages)
df['lag_24h'] = consommation.shift(48)   # t-48 pas = t-24h
df['lag_48h'] = consommation.shift(96)   # t-96 pas = t-48h
df['lag_7d']  = consommation.shift(336)  # t-336 pas = t-7 jours

# 4. Moyennes glissantes thermiques (inertie thermique des bâtiments)
df['temp_roll_mean_3h'] = temperature.rolling(6).mean()   # 6 pas × 30min = 3h
df['temp_roll_mean_6h'] = temperature.rolling(12).mean()  # 12 pas × 30min = 6h
```

**Gestion des NaN (différence entraînement/inférence) :**

| Mode | Comportement | Raison |
|:---|:---|:---|
| `is_training=True` | `dropna()` sur les lags | Les premières 7 jours n'ont pas de lag_7d valide |
| `is_training=False` | `bfill().fillna(mean)` | En production, on impute plutôt que de rejeter |

#### C. Normalisation — `fit_transform()` et `transform()`

```python
# Ajustement (UNIQUEMENT sur données d'entraînement)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)  # μ et σ calculés ici

# Application (sur données de test ou de production)
X_scaled = scaler.transform(X_test)        # Utilise μ et σ du train
```

> [!CAUTION]
> Il est crucial de ne **jamais** appeler `fit_transform()` sur les données de test ou de production. Cela introduirait une fuite de données (data leakage) et invaliderait l'évaluation. Seule la méthode `transform()` doit être utilisée en inférence.

---

### 1.4 Services de Déploiement

#### A. API FastAPI — `src/api/app.py`

**Endpoints disponibles :**

```
┌─────────────────────────────────────────────────────────────────────┐
│  POST /predict                                                       │
│  ─────────────────────────────────────────────────────────────────  │
│  Corps (JSON) :                                                      │
│    datetime*      : str   ISO 8601 ("2026-05-27T18:30:00")          │
│    temperature*   : float Température nationale moyenne (°C)         │
│    lag_24h        : float [optionnel] Consommation t-24h (MW)       │
│    lag_48h        : float [optionnel] Consommation t-48h (MW)       │
│    lag_7d         : float [optionnel] Consommation t-7j (MW)        │
│    temp_roll_mean_3h : float [optionnel] Moy. glissante 3h          │
│    temp_roll_mean_6h : float [optionnel] Moy. glissante 6h          │
│                                                                      │
│  Réponse (JSON) :                                                    │
│    datetime       : str   Horodatage de la prédiction               │
│    prediction_mw  : float Consommation prédite en MW                │
│    status         : str   "success"                                  │
│    model_used     : str   Nom de la classe du modèle actif          │
│    latency_sec    : float Temps d'inférence en secondes             │
│                                                                      │
│  Codes d'erreur :                                                    │
│    400  Format datetime invalide                                     │
│    503  Modèle non initialisé                                        │
│    500  Erreur d'inférence interne                                   │
├─────────────────────────────────────────────────────────────────────┤
│  GET /health                                                         │
│  → {"status": "ok"}        si modèle chargé                         │
│  → {"status": "unhealthy"} si modèle absent                         │
├─────────────────────────────────────────────────────────────────────┤
│  GET /metrics                                                        │
│  → Métriques Prometheus (text/plain)                                 │
│     http_requests_total{method,endpoint,http_status}                │
│     inference_latency_seconds{bucket,sum,count}                     │
│     predicted_consumption_megawatts                                  │
└─────────────────────────────────────────────────────────────────────┘
```

**Comportement au démarrage (`@app.on_event("startup")`) :**

```python
def startup_event():
    # 1. Tentative de chargement des artefacts depuis models/
    if os.path.exists("models/best_model.joblib"):
        model = joblib.load("models/best_model.joblib")
        pipeline = joblib.load("models/data_pipeline.joblib")
    else:
        # 2. Auto-entraînement de secours (si aucun modèle présent)
        run_training()  # Génère et entraîne sur 180j synthétiques
        model = joblib.load("models/best_model.joblib")
```

#### B. Dockerfile — Construction Multi-Étapes

```dockerfile
# ═══ ÉTAPE 1 : BUILDER (compilation des dépendances) ═══
FROM python:3.10-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential  # gcc pour scipy/numpy
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt
# Résultat : /root/.local/ (packages Python compilés)

# ═══ ÉTAPE 2 : RUNNER (image de production légère) ═══
FROM python:3.10-slim AS runner
WORKDIR /app

# Utilisateur non-privilégié (sécurité)
RUN groupadd -g 999 appuser && useradd -r -u 999 -g appuser appuser

# Copie uniquement les packages compilés (pas les outils de build)
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Copie du code source uniquement (pas les données ou secrets)
COPY src/ /app/src/
RUN mkdir -p /app/models && chown -R appuser:appuser /app

USER appuser
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# Sonde de santé Docker native
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Bénéfices de l'approche multi-stage :**
- **Image finale ~60% plus légère** : `build-essential` et outils de compilation absents du runner
- **Sécurité** : Exécution sous utilisateur non-root (uid 999), aucune élévation de privilèges
- **Reproductibilité** : Image basée sur `python:3.10-slim` avec version fixée

#### C. Manifestes Kubernetes

| Fichier | Ressource | Rôle |
|:---|:---:|:---|
| `k8s/deployment.yaml` | `Deployment` | 3 répliques, RollingUpdate (maxUnavailable=0), limites CPU/RAM |
| `k8s/service.yaml` | `Service (LoadBalancer)` | Exposition externe port 80 → pod 8000 |
| `k8s/hpa.yaml` | `HorizontalPodAutoscaler` | Auto-scaling 3→10 pods selon CPU (seuil 70%) |

**Flux d'une requête en production :**
```
Internet → LoadBalancer (port 80)
         → Service K8s (edf-consumption-predictor-service)
         → Round-Robin vers 1 des 3–10 pods
         → FastAPI Uvicorn (port 8000)
         → Chargement modèle depuis /app/models/best_model.joblib
         → Réponse JSON
```

---

### 1.5 Pipeline CI/CD — GitHub Actions (`.github/workflows/ci_cd.yml`)

Le pipeline CI/CD s'exécute automatiquement sur chaque **push** ou **pull request** sur la branche `main`. Il comporte **4 jobs séquentiels** :

```
Push/PR → main
    │
    ▼
┌─────────────────────────────┐
│  Job 1 : lint-and-quality   │  ~2 min
│  ─────────────────────────  │
│  • Black (formatage)         │
│  • Flake8 (erreurs Python)   │
│  • Mypy (typage statique)    │
└──────────────┬──────────────┘
               │ (si OK)
               ▼
┌─────────────────────────────┐
│  Job 2 : unit-tests         │  ~5 min
│  ─────────────────────────  │
│  • pytest tests/            │
│  • pytest-cov (couverture)  │
│  • httpx (client test API)  │
└──────────────┬──────────────┘
               │ (si OK)
               ▼
┌─────────────────────────────┐
│  Job 3 : security-scans     │  ~3 min
│  ─────────────────────────  │
│  • Bandit (vulnérabilités   │
│    Python : SQL inject,     │
│    eval(), etc.)             │
│  • Trivy (CVE filesystem)   │
└──────────────┬──────────────┘
               │ (si OK + push sur main uniquement)
               ▼
┌─────────────────────────────┐
│  Job 4 : build-and-push     │  ~8 min
│  ─────────────────────────  │
│  • Docker Buildx             │
│  • Login Azure Container    │
│    Registry (secrets CI)    │
│  • Push :latest + :sha       │
│  • Scan Trivy sur image      │
└─────────────────────────────┘
```

**Secrets GitHub requis :**

| Secret | Description |
|:---|:---|
| `REGISTRY_USERNAME` | Login Azure Container Registry (ACR) |
| `REGISTRY_PASSWORD` | Mot de passe / token ACR |

> [!IMPORTANT]
> Les secrets ne sont **jamais** exposés dans les logs CI/CD. GitHub Actions les masque automatiquement. Ne jamais les écrire en clair dans le code ou les fichiers de configuration.

---

### 1.6 Prérequis Techniques

#### A. Environnement de Développement (DEV)

| Prérequis | Version minimale | Version testée | Note |
|:---|:---:|:---:|:---|
| **Python** | 3.10 | 3.10.x | 3.11+ non testé (compatibilité scikit-learn) |
| **pip** | 22.x | 24.x | `python -m pip install --upgrade pip` |
| **Docker** | 20.10 | 26.x | Pour les builds et tests conteneurisés |
| **Git** | 2.30 | 2.45 | Pour le versionnement et CI/CD |

#### B. Librairies Python (`requirements.txt`)

| Librairie | Version minimale | Rôle |
|:---|:---:|:---|
| `pandas` | ≥ 1.5.0 | Manipulation des DataFrames temporels |
| `numpy` | ≥ 1.22.0 | Calcul vectoriel, encodages cycliques |
| `scikit-learn` | ≥ 1.0.0 | Modèles ML, StandardScaler, métriques |
| `fastapi` | ≥ 0.95.0 | Framework API REST asynchrone |
| `uvicorn` | ≥ 0.20.0 | Serveur ASGI pour FastAPI |
| `prometheus-client` | ≥ 0.16.0 | Exposition métriques `/metrics` |
| `requests` | ≥ 2.28.0 | Appels API externe (ODRE RTE) |
| `holidays` | ≥ 0.20 | Calendrier jours fériés français |
| `evidently` | ≥ 0.2.0 | Rapports HTML de dérive de données |
| `locust` | ≥ 2.15.0 | Tests de charge virtuels |
| `pytest` | ≥ 7.2.0 | Framework de tests unitaires |
| `matplotlib` | ≥ 3.6.0 | Visualisation des analyses |
| `shap` | ≥ 0.41.0 | Explainability des prédictions |
| `joblib` | ≥ 1.2.0 | Sérialisation rapide des modèles |
| `pydantic` | ≥ 1.10.0 | Validation des schémas d'entrée/sortie |
| `scipy` | (transitive) | Test KS-2samp pour la dérive |

**Installation :**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### C. Ressources Minimales

**Instance de développement (1 réplique) :**
| Ressource | Minimum | Recommandé |
|:---|:---:|:---:|
| CPU | 1 vCPU | 2 vCPU |
| RAM | 512 MB | 1 GB |
| Disque | 500 MB | 2 GB |
| Réseau | LAN local | — |

**Cluster de production (3 répliques + HPA) :**
| Ressource | Par pod (request/limit) | Total cluster (3 pods) |
|:---|:---:|:---:|
| CPU | 200m / 500m | 0,6 / 1,5 vCPU |
| RAM | 256 MB / 512 MB | 768 MB / 1,5 GB |
| Disque | — (modèle : ~1,5 MB) | — |

**Compatibilité OS :**
- ✅ Linux (Ubuntu 20.04+, Debian 11+) — Recommandé pour Docker et K8s
- ✅ macOS 12+ (développement local, tests)
- ✅ Windows 10/11 avec WSL2 (développement local)

---

## 2. Runbook d'Exploitation

> [!NOTE]
> Ce runbook constitue le guide pas-à-pas pour les opérateurs. Chaque procédure est autonome et peut être exécutée indépendamment. Les commandes supposent un accès `kubectl` configuré sur le cluster `edf-rte-production`.

---

### 2.1 Démarrer la Solution

#### Environnement de Développement (local)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. (Optionnel) Entraîner les modèles si absent
python -m src.models.train_evaluate

# 3. Démarrer l'API localement
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload

# 4. Vérifier que l'API répond
curl http://localhost:8000/health
# Attendu : {"status": "ok"}
```

#### Environnement Conteneurisé (Docker)

```bash
# 1. Construire l'image Docker
docker build -t predictor-api:dev .

# 2. Lancer le conteneur
docker run -d \
  --name predictor-api \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \  # Monte les modèles existants
  predictor-api:dev

# 3. Vérifier la santé du conteneur
docker ps
docker logs predictor-api --tail=20

# 4. Tester l'endpoint
curl http://localhost:8000/health
```

#### Environnement Production (Kubernetes)

```bash
# 1. Appliquer tous les manifestes (dans l'ordre : deployment → service → hpa)
kubectl apply -f k8s/deployment.yaml -n edf-rte-production
kubectl apply -f k8s/service.yaml    -n edf-rte-production
kubectl apply -f k8s/hpa.yaml        -n edf-rte-production

# 2. Vérifier le démarrage des pods (attendre ~30s)
kubectl get pods -n edf-rte-production -l app=edf-consumption-predictor -w

# 3. Vérifier l'état du déploiement
kubectl rollout status deployment/edf-consumption-predictor-api -n edf-rte-production
# Attendu : "deployment successfully rolled out"

# 4. Récupérer l'adresse IP du service LoadBalancer
kubectl get service edf-consumption-predictor-service -n edf-rte-production
# → Colonne EXTERNAL-IP

# 5. Tester depuis l'extérieur
curl http://<EXTERNAL-IP>/health
```

**État de démarrage nominal :**
```
$ kubectl get pods -n edf-rte-production
NAME                                              READY   STATUS    RESTARTS   AGE
edf-consumption-predictor-api-6d8f9c-abc12        1/1     Running   0          45s
edf-consumption-predictor-api-6d8f9c-def34        1/1     Running   0          45s
edf-consumption-predictor-api-6d8f9c-ghi56        1/1     Running   0          45s
```

---

### 2.2 Arrêter la Solution

#### Arrêt complet (suppression des ressources K8s)

```bash
# ATTENTION : Supprime le service et coupe le trafic immédiatement
kubectl delete -f k8s/hpa.yaml        -n edf-rte-production
kubectl delete -f k8s/service.yaml    -n edf-rte-production
kubectl delete -f k8s/deployment.yaml -n edf-rte-production

# Vérifier que tous les pods ont bien été supprimés
kubectl get pods -n edf-rte-production
# Attendu : "No resources found in edf-rte-production namespace."
```

#### Mise en pause temporaire (scale-down à 0 répliques)

```bash
# Mise en pause sans suppression des ressources
kubectl scale deployment/edf-consumption-predictor-api \
  --replicas=0 -n edf-rte-production

# Vérifier
kubectl get deployment/edf-consumption-predictor-api -n edf-rte-production
# Attendu : READY 0/0

# Redémarrer (revenir à 3 répliques)
kubectl scale deployment/edf-consumption-predictor-api \
  --replicas=3 -n edf-rte-production
```

#### Arrêt du conteneur Docker (DEV)

```bash
docker stop predictor-api
docker rm predictor-api
```

---

### 2.3 Déployer une Nouvelle Version de Modèle

#### Scénario A — Déploiement automatique via CI/CD (voie normale)

```
Développeur → git push origin main
           → GitHub Actions déclenché automatiquement
           → Job 1 : Lint (Black, Flake8, Mypy)
           → Job 2 : Tests (pytest --cov)
           → Job 3 : Sécurité (Bandit, Trivy)
           → Job 4 : Build + Push image Docker avec tag :sha et :latest
           → Mise à jour Kubernetes automatique (si configuré avec ArgoCD/Flux)
```

**Durée totale estimée :** ~18 minutes (lint 2min + tests 5min + scan 3min + build 8min)

#### Scénario B — Déploiement manuel d'une version spécifique

```bash
# 1. Spécifier la version exacte à déployer (utiliser le SHA de commit ou un tag sémantique)
export NEW_VERSION="v1.2.3"
# ou
export NEW_VERSION="sha-a3b2c1d"

# 2. Mettre à jour l'image du déploiement
kubectl set image deployment/edf-consumption-predictor-api \
  predictor-api=edf-rte-registry.azurecr.io/predictor-api:${NEW_VERSION} \
  -n edf-rte-production

# 3. Suivre la progression du Rolling Update
kubectl rollout status deployment/edf-consumption-predictor-api -n edf-rte-production
# La mise à jour est sans interruption (maxUnavailable: 0, maxSurge: 1)
# Durée : ~30-60 secondes selon le temps de démarrage des pods

# 4. Valider post-déploiement (checks essentiels)
kubectl get pods -n edf-rte-production  # Tous READY 1/1
curl http://<EXTERNAL-IP>/health         # {"status": "ok"}
curl -X POST http://<EXTERNAL-IP>/predict \
  -H "Content-Type: application/json" \
  -d '{"datetime":"2026-06-03T14:00:00","temperature":18.5}'
# Vérifier : prediction_mw > 0, status = "success", latency_sec < 0.1
```

#### Scénario C — Mise à jour du seul modèle ML (sans rebuilder l'image)

```bash
# 1. Déclencher manuellement le DAG Airflow de ré-entraînement
#    (Interface Web Airflow → DAG : edf_consumption_predictor_retraining → Trigger)

# 2. Ou via la CLI Airflow
airflow dags trigger edf_consumption_predictor_retraining

# 3. Suivre les 3 tâches du DAG dans l'interface Airflow
#    extract_and_prepare_data → train_challenger → evaluate_and_compare

# 4. Si le challenger est promu, les fichiers sont mis à jour :
#    models/best_model.joblib
#    models/data_pipeline.joblib

# 5. Redémarrer les pods pour recharger le nouveau modèle en mémoire
kubectl rollout restart deployment/edf-consumption-predictor-api -n edf-rte-production
kubectl rollout status deployment/edf-consumption-predictor-api -n edf-rte-production
```

---

### 2.4 Rollback d'Urgence

> [!CAUTION]
> Cette procédure doit être exécutée dès qu'une anomalie critique est détectée (taux d'erreur HTTP 500 > 1%, latence P95 > 1s, prédictions manifestement aberrantes). La cible est un retour à la normale en moins de 30 secondes.

#### Rollback Niveau 1 — API/Code (retour à la version précédente de l'image)

```bash
# Retour immédiat à la version précédente
kubectl rollout undo deployment/edf-consumption-predictor-api -n edf-rte-production

# Suivre le rollback
kubectl rollout status deployment/edf-consumption-predictor-api -n edf-rte-production

# Vérifier l'image désormais utilisée
kubectl describe deployment/edf-consumption-predictor-api -n edf-rte-production | grep Image

# Valider le retour à la normale
curl http://<EXTERNAL-IP>/health
```

**Historique des révisions disponibles :**
```bash
kubectl rollout history deployment/edf-consumption-predictor-api -n edf-rte-production
# Affiche la liste des révisions avec leur image
# Exemple :
# REVISION  CHANGE-CAUSE
# 1         predictor-api=edf-rte-registry.azurecr.io/predictor-api:v1.0.0
# 2         predictor-api=edf-rte-registry.azurecr.io/predictor-api:v1.1.0
# 3         predictor-api=edf-rte-registry.azurecr.io/predictor-api:v1.2.0  ← actuel
```

#### Rollback Niveau 2 — Modèle ML (retour à une version précédente du modèle)

```bash
# 1. Lister les sauvegardes de modèles disponibles dans le stockage
ls -la models/
# best_model.joblib           ← Version actuelle (corrompue/dégradée)
# best_model_backup_2026-05-20.joblib  ← Backup précédente

# 2. Restaurer la version saine
cp models/best_model_backup_2026-05-20.joblib models/best_model.joblib
cp models/data_pipeline_backup_2026-05-20.joblib models/data_pipeline.joblib

# 3. Forcer le rechargement du modèle dans les pods
kubectl rollout restart deployment/edf-consumption-predictor-api -n edf-rte-production

# 4. Valider
curl -X POST http://<EXTERNAL-IP>/predict \
  -H "Content-Type: application/json" \
  -d '{"datetime":"2026-06-03T14:00:00","temperature":18.5}'
```

#### Rollback Niveau 3 — Infrastructure complète (cas extrême)

```bash
# Si tout le namespace est dans un état incohérent :
# 1. Supprimer et recréer toutes les ressources
kubectl delete namespace edf-rte-production
kubectl create namespace edf-rte-production

# 2. Réappliquer tous les manifestes
kubectl apply -f k8s/ -n edf-rte-production
```

---

### 2.5 Checks Essentiels — Vérifier que Tout Fonctionne

Ces vérifications doivent être exécutées :
- Après chaque déploiement d'une nouvelle version
- Après chaque rollback
- Chaque matin par l'équipe Ops (surveillance quotidienne)

#### Check 1 — Santé des Pods

```bash
kubectl get pods -n edf-rte-production -l app=edf-consumption-predictor
# ✅ Attendu : 3 pods en statut Running, READY 1/1, RESTARTS = 0
# ❌ Problème si : CrashLoopBackOff, OOMKilled, Error, RESTARTS > 0
```

#### Check 2 — Sonde de Vie API

```bash
curl -s http://<EXTERNAL-IP>/health | python3 -m json.tool
# ✅ Attendu : {"status": "ok"}
# ❌ Problème si : {"status": "unhealthy"} → modèle non chargé
```

#### Check 3 — Inférence de Bout en Bout

```bash
curl -s -X POST http://<EXTERNAL-IP>/predict \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": "2026-06-03T14:00:00",
    "temperature": 18.5,
    "lag_24h": 52000.0,
    "lag_48h": 51500.0,
    "lag_7d": 53000.0
  }' | python3 -m json.tool

# ✅ Attendu :
# {
#   "prediction_mw": ~48000–65000,  (plausible pour 18°C en été)
#   "status": "success",
#   "model_used": "KNeighborsRegressor",
#   "latency_sec": < 0.1
# }
# ❌ Problème si : latency_sec > 0.5, prediction_mw < 0 ou > 150000
```

#### Check 4 — Métriques Prometheus

```bash
curl -s http://<EXTERNAL-IP>/metrics | grep "inference_latency"
# ✅ Attendu : présence de inference_latency_seconds_count > 0
# ✅ Attendu : inference_latency_seconds_bucket{le="0.05"} représente ~99% des requêtes

curl -s http://<EXTERNAL-IP>/metrics | grep "http_requests_total"
# ✅ Attendu : http_requests_total{http_status="200"} >> http_requests_total{http_status="500"}
```

#### Check 5 — HPA (Autoscaler)

```bash
kubectl get hpa -n edf-rte-production
# ✅ Attendu :
# NAME                              MINPODS   MAXPODS   REPLICAS   CPU
# edf-consumption-predictor-hpa    3         10        3          <70%
```

#### Check 6 — Logs (Absence d'erreurs)

```bash
kubectl logs deployment/edf-consumption-predictor-api \
  -n edf-rte-production --tail=50

# ✅ Attendu : "Model and pipeline successfully loaded."
# ❌ À surveiller : "Error auto-training", "Inference error", Traceback Python
```

#### Checklist de Validation Post-Déploiement

```
□ Check 1 : 3 pods Running, 0 RESTARTS
□ Check 2 : GET /health → {"status": "ok"}
□ Check 3 : POST /predict → prediction_mw plausible, latency_sec < 0.1
□ Check 4 : GET /metrics → métriques présentes et cohérentes
□ Check 5 : HPA → REPLICAS = 3, CPU < 70%
□ Check 6 : Logs → aucune erreur critique
□ Check 7 : Dashboard Grafana → pas d'alerte rouge
```

---

## 3. Gestion des Incidents

### 3.1 Incident A — Chute de Performances du Modèle

**Symptômes :**
- Dashboard Grafana : MAPE > 6% sur les 24 dernières heures
- Alertes Prometheus : `http_requests_total{http_status="500"}` en augmentation
- Feedback utilisateurs : prédictions aberrantes (ex: 150 000 MW en été)

**Arbre de décision :**

```
[ALERTE : MAPE > 6%]
│
├── Étape 1 : Vérifier si le modèle actif est le bon
│   kubectl exec <pod> -n edf-rte-production -- ls -la /app/models/
│   → Présence de best_model.joblib ? Taille > 1 MB ?
│
├── Étape 2 : Vérifier les logs d'inférence
│   kubectl logs -n edf-rte-production deploy/edf-consumption-predictor-api --tail=100
│   → Erreurs de type "Inference error" ? Valeurs NaN dans les features ?
│
├── Étape 3 : Vérifier le rapport de dérive
│   cat models/drift_report.json
│   → drift_detected: true avec KS-stat > 0.6 ?
│   OUI → Déclencher ré-entraînement urgent (voir §2.3 Scénario C)
│   NON → Continuer
│
├── Étape 4 : Vérifier la qualité des données d'entrée
│   → Les features d'entrée (température, lags) sont-elles dans des plages normales ?
│   → Données manquantes remplacées par des valeurs par défaut incorrectes ?
│
└── Étape 5 : Escalade Data Science (Niveau 3)
    → Ouvrir un ticket avec les métriques observées, le drift_report.json et les logs
    → Analyse des données source RTE : changement de comportement structurel ?
```

**Actions :**

| Action | Commande | Délai estimé |
|:---|:---|:---:|
| Vérifier dérive | `cat models/drift_report.json` | < 1 min |
| Déclencher ré-entraînement | `airflow dags trigger edf_consumption_predictor_retraining` | 5-10 min |
| Rollback modèle précédent | `cp best_model_backup.joblib best_model.joblib` + `kubectl rollout restart` | < 2 min |
| Escalade Data Science | Ticket Jira/Teams avec logs | < 5 min |

**→ Référence croisée :** Voir Livrable 1, Section 2.3 (Détection de dérive) et 2.4 (Ré-entraînement).

---

### 3.2 Incident B — Service Ne Répond Plus (API Muette)

**Symptômes :**
- `curl http://<IP>/health` → timeout ou `Connection refused`
- Dashboard Grafana : débit (req/s) = 0
- Alertes Uptime : SLA en danger

**Arbre de décision :**

```
[ALERTE : Service indisponible]
│
├── Étape 1 : Vérifier l'état des pods
│   kubectl get pods -n edf-rte-production
│   │
│   ├── CrashLoopBackOff → Consulter logs : kubectl logs <pod> --previous
│   │   Cause probable : erreur démarrage (modèle corrompu, manque mémoire)
│   │   Action : kubectl rollout undo (rollback vers version stable)
│   │
│   ├── OOMKilled (Exit Code 137) → Augmenter les limites mémoire (512Mi → 1Gi)
│   │   kubectl edit deployment/edf-consumption-predictor-api -n edf-rte-production
│   │
│   ├── Pending (pas de ressources) → Vérifier la capacité du cluster
│   │   kubectl describe nodes | grep "Allocated resources"
│   │
│   └── Running 0/3 → Les pods existent mais ne sont pas prêts
│       kubectl describe pod <pod> -n edf-rte-production
│       → readinessProbe échouée ? Port 8000 non accessible ?
│
├── Étape 2 : Vérifier le LoadBalancer
│   kubectl get service -n edf-rte-production
│   → EXTERNAL-IP "pending" ? Problème de provisionnement Azure
│
└── Étape 3 : Redémarrer manuellement
    kubectl rollout restart deployment/edf-consumption-predictor-api -n edf-rte-production
```

**Actions selon le diagnostic :**

| Diagnostic | Action | Commande |
|:---|:---|:---|
| `CrashLoopBackOff` | Rollback API | `kubectl rollout undo deployment/...` |
| `OOMKilled` | Augmenter RAM | Éditer `deployment.yaml`, relancer `kubectl apply` |
| `503` sur /predict | Modèle absent | `kubectl exec <pod> -- python -m src.models.train_evaluate` |
| LoadBalancer pending | Vérifier Azure | Ouvrir un ticket Azure Support |

**→ Référence croisée :** Voir RUNBOOK.md du projet (Incident C — Erreur 503) et Livrable 1, Section 1.4.

---

### 3.3 Incident C — Dérive de Données Détectée

**Symptômes :**
- Rapport Grafana : indicateur drift en orange ou rouge
- `cat models/drift_report.json` → `drift_detected: true`, KS-stat > 0.6
- MAPE en hausse progressive sur 3-5 jours consécutifs

**Contexte de la dérive :**

```
KS-stat [0.0 – 0.3]  → Distribution stable → Monitoring standard
KS-stat [0.3 – 0.6]  → Dérive modérée (saisonnière) → Ré-entraînement planifié
KS-stat [0.6 – 1.0]  → Dérive sévère (événement climatique) → Action immédiate
```

**Procédure :**

```bash
# 1. Consulter le rapport de dérive détaillé
cat models/drift_report.json

# 2. Identifier la/les variable(s) driftée(s)
python3 -c "
import json
with open('models/drift_report.json') as f:
    report = json.load(f)
for feature, result in report['drifted_scenario'].items():
    if result['drift_detected']:
        print(f'DÉRIVE : {feature} | KS={result[\"statistic\"]:.3f} | p={result[\"p_value\"]:.2e}')
"

# 3. Si dérive confirmée → Déclencher le ré-entraînement immédiat
airflow dags trigger edf_consumption_predictor_retraining

# 4. Suivre l'exécution dans l'interface Airflow
# → Attendre la tâche evaluate_and_compare
# → Vérifier si le challenger a été promu

# 5. Valider post-ré-entraînement
python3 -c "
import json
with open('models/mlflow_logs.json') as f:
    logs = json.load(f)
best = min(logs, key=lambda k: logs[k]['MAPE'])
print(f'Nouveau champion : {best} | MAPE : {logs[best][\"MAPE\"]*100:.2f}%')
"
```

**→ Référence croisée :** Voir Livrable 1, Section 2.3 (Détection de dérive) et RUNBOOK.md Incident B.

---

### 3.4 Incident D — Changement de Format des Données Entrantes

**Symptômes :**
- Erreurs HTTP 400 en masse sur `/predict`
- Logs : `Invalid datetime format` ou `KeyError` dans le pipeline
- Les clients signalent que leurs appels échouent malgré un payload correct

**Causes possibles :**
1. Changement de format datetime dans le système source (ex: `"2026-06-03 14:00"` au lieu de `"2026-06-03T14:00:00"`)
2. Modification du nom des champs JSON (ex: `"temp"` au lieu de `"temperature"`)
3. Changement d'unité des données (ex: température en Kelvin au lieu de Celsius)
4. Ajout de champs obligatoires par erreur dans le schéma Pydantic

**Procédure :**

```bash
# 1. Reproduire l'erreur en local
curl -v -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"datetime":"2026-06-03 14:00","temperature":18.5}'
# → Lire le message d'erreur détaillé dans la réponse

# 2. Inspecter le schéma Pydantic attendu
python3 -c "
from src.api.app import PredictRequest
import json
print(json.dumps(PredictRequest.schema(), indent=2))
"

# 3a. Si le changement vient du CLIENT (API consommatrice)
#     → Leur transmettre la documentation du schéma attendu
#     → Ou adapter leur code pour envoyer le bon format

# 3b. Si le changement vient de NOUS (évolution volontaire du schéma)
#     → Versionner l'API (v2/ prefix)
#     → Maintenir la compatibilité ascendante pendant une période de transition

# 3c. Adapter le code si le changement est structurel et vient des données source
#     → Modifier data_pipeline.py pour le nouveau format
#     → Écrire un test de régression, merger via PR + CI/CD
```

**Règle d'or : ne jamais casser la compatibilité ascendante sans versionner l'API.**

---

### 3.5 Incident E — Mémoire Insuffisante (OOMKilled)

**Symptômes :**
- `kubectl get pods` : statut `OOMKilled`, Exit Code `137`
- Les pods se redémarrent en boucle (CrashLoopBackOff après plusieurs OOM)
- Grafana : pic de consommation RAM > 512 MB

**Procédure :**

```bash
# 1. Confirmer le diagnostic OOM
kubectl describe pod <pod-name> -n edf-rte-production | grep -A5 "Last State"
# → "OOMKilled"

# 2. Augmenter les limites de ressources
kubectl edit deployment/edf-consumption-predictor-api -n edf-rte-production
# Modifier :
#   resources:
#     requests:
#       memory: "512Mi"    ← était 256Mi
#     limits:
#       memory: "1Gi"      ← était 512Mi

# 3. Ou appliquer via le fichier YAML modifié
kubectl apply -f k8s/deployment.yaml -n edf-rte-production

# 4. Vérifier la stabilisation
kubectl get pods -n edf-rte-production -w
# Attendre que les 3 pods soient Running sans RESTARTS supplémentaires
```

**→ Référence croisée :** Voir RUNBOOK.md du projet (Incident A — OOMKilled) et Livrable 1, Section 3.4 (Risques).

---

## 4. Références Croisées — Livrable 1

Ce document doit être utilisé conjointement avec le **Livrable 1 — Dossier de Déploiement & de Maintenabilité** selon la correspondance suivante :

| Sujet | Ce document (Livrable 2) | Livrable 1 |
|:---|:---:|:---:|
| Architecture globale et schémas | §1.1 | §1.1, 1.2 |
| Description technique des modèles | §1.2 | §1.2.B |
| Pipeline de données | §1.3 | §1.2.A |
| Dockerfile et sécurité | §1.4.B | §1.4 |
| CI/CD | §1.5 | §1.3 (env. TEST) |
| Prérequis techniques | §1.6 | — |
| Procédure démarrage/arrêt | §2.1, 2.2 | — |
| Déploiement nouvelle version | §2.3 | §2.4 (versionnement) |
| Rollback | §2.4 | §2.4.D |
| Checks essentiels | §2.5 | §2.2 (métriques) |
| Gestion incidents performances | §3.1 | §2.1, 2.2, 2.4 |
| Gestion incidents disponibilité | §3.2 | §2.1.B, 2.1.C |
| Gestion incidents dérive | §3.3 | §2.3 (dérive) |
| Rôles et responsabilités | — | §2.6 (RACI) |
| Tests de charge | — | §3.1 – 3.4 |
| Préconisations pour la prod | §5 | §3.4.C |

---

## 5. Note d'Expertise Technique à l'Équipe Projet

### 5.1 Choix Techniques Clés — Justifications

#### Choix 1 — KNeighbors comme modèle champion plutôt que Random Forest ou RBFN

**Décision :** KNeighbors (k=5, weights='distance') a été sélectionné comme modèle de production.

**Justification :**
- **MAPE le plus bas** (4,68% vs 4,87% pour Random Forest), ce qui est déterminant pour la criticité métier des prédictions de consommation nationale
- **Temps d'inférence quasi-nul** (< 1 ms) : aucune décomposition d'arbre, aucun calcul matriciel complexe — juste une recherche de voisins sur un petit espace normalisé
- **Pas de surapprentissage** avec k=5 : le modèle est naturellement régularisé par l'agrégation de 5 voisins pondérés
- **Comportement prévisible** : en production, les nouvelles données de consommation sont toujours proches des données historiques récentes (lags). KNN exploite parfaitement cette propriété de continuité temporelle

> [!TIP]
> En production ML industrielle, la stabilité et la prédictibilité d'un modèle comptent souvent davantage que quelques dixièmes de point de MAPE. Un RandomForest plus performant sur le papier mais dont les prédictions varient davantage entre les versions peut être moins fiable en opération.

#### Choix 2 — FastAPI + Uvicorn plutôt que Flask ou Django

**Décision :** FastAPI avec serveur ASGI Uvicorn.

**Justification :**
- **Validation automatique** des entrées/sorties via les schémas Pydantic (`PredictRequest`, `PredictResponse`) — pas de code de validation manuel sujet aux bugs
- **Documentation OpenAPI générée automatiquement** (`/docs`, `/redoc`) — indispensable pour les équipes consommatrices de l'API
- **Asynchrone natif (async/await)** — meilleure gestion de la concurrence sous charge sans threading complexe
- **Prometheus intégré facilement** via `prometheus-client` — exposition `/metrics` en 5 lignes de code

#### Choix 3 — Dockerfile multi-stage pour la sécurité et la légèreté

**Décision :** Construction en deux étapes (builder + runner).

**Justification :**
- L'image finale ne contient **pas `gcc`, `build-essential`** ni les outils de compilation — surface d'attaque réduite d'environ 60% en taille
- Les **CVE des outils de build** ne sont pas présents dans l'image de production (scannée par Trivy)
- L'utilisateur `appuser` (uid 999, non-root) empêche les attaques d'escalade de privilèges

#### Choix 4 — StandardScaler plutôt que MinMaxScaler ou RobustScaler

**Décision :** `StandardScaler` (normalisation Z-score).

**Justification :**
- **KNN est sensible aux échelles** : sans normalisation, la variable `consommation` (ordre 50 000 MW) écraserait complètement la variable `hour_sin` (ordre [-1, 1])
- `StandardScaler` est optimal pour KNN car il préserve la forme des distributions sans les comprimer dans [0,1] (ce que ferait MinMaxScaler et qui pénaliserait les outliers)
- La **clé de la reproductibilité** : le scaler est sérialisé avec le modèle dans `data_pipeline.joblib`, garantissant que les mêmes statistiques de normalisation (μ, σ) sont appliquées en inférence qu'en entraînement

#### Choix 5 — Encodages cycliques sinus/cosinus pour les variables temporelles

**Décision :** `hour_sin = sin(2π × heure / 24)` plutôt que l'heure brute (0-23).

**Justification :**
- L'heure brute `23` et `0` sont proches temporellement (1h d'écart) mais loin numériquement (23 unités d'écart). Un modèle ML naïf pensera qu'ils sont dissimilaires, causant des erreurs aux transitions minuit/6h.
- Les encodages cycliques font en sorte que **23h et 0h ont des vecteurs (sin, cos) proches**, ce qui est physiquement correct.
- Le même raisonnement s'applique aux mois : décembre (12) et janvier (1) sont numériquement loin mais climatiquement proches.

#### Choix 6 — Lags temporels (t-24h, t-48h, t-7j) comme features critiques

**Décision :** Inclure la consommation passée comme variable explicative.

**Justification :**
- La consommation électrique est **fortement auto-corrélée** : ce qui s'est passé hier à la même heure est le meilleur prédicteur de ce qui va se passer aujourd'hui
- Le lag à 7 jours capture la **cyclicité hebdomadaire** (les lundis se ressemblent entre eux)
- Sans ces lags, un simple modèle de température ne capturerait pas les variations dues aux comportements humains (vacances, grèves, événements sportifs)

#### Choix 7 — Pipeline Champion/Challenger pour le ré-entraînement automatique

**Décision :** Ne jamais remplacer le modèle en production sans le comparer au champion actuel sur les mêmes données de test.

**Justification :**
- Le ré-entraînement automatique **sans validation** pourrait dégrader les performances si les nouvelles données sont trop atypiques (canicule extrême, panne nationale)
- La règle `mape_chal < mape_champ AND mape_chal <= 0.05` garantit que **seule une amélioration réelle** déclenche une mise en production — protégeant ainsi contre les régressions silencieuses

#### Choix 8 — Test de Kolmogorov-Smirnov pour la détection de dérive

**Décision :** KS-2samp de SciPy comme test statistique de dérive.

**Justification :**
- **Non-paramétrique** : ne suppose pas une distribution normale — important car la consommation électrique a une distribution bimodale (pics matinaux/vespéraux)
- **Sensible aux changements de forme** de la distribution (pas seulement de la moyenne), ce qui est crucial pour détecter des dérives structurelles
- Interprétation claire : p_value < 0.05 → les deux distributions sont statistiquement différentes (avec 95% de confiance)

#### Choix 9 — Gestion gracieuse des champs optionnels dans l'API

**Décision :** Les lags et moyennes glissantes sont optionnels dans `PredictRequest`, avec des valeurs par défaut raisonnables (55 000 MW, température actuelle).

**Justification :**
- **Facilite l'intégration** : les systèmes clients n'ont pas toujours accès aux données historiques en temps réel
- **Robustesse en production** : évite les erreurs 422 pour des champs non critiques
- Les valeurs par défaut (55 000 MW) correspondent à la consommation moyenne nationale annuelle, ce qui est un fallback raisonnable

#### Choix 10 — CI/CD en 4 étapes séquentielles avec gate quality

**Décision :** Chaque étape du pipeline CI/CD doit réussir avant que la suivante s'exécute (`needs:` Airflow).

**Justification :**
- **Fail fast** : une faute de style (Black) ou une erreur de type (Mypy) est détectée en 2 minutes, avant d'attendre le build Docker (8 minutes)
- Le **scan de sécurité Bandit + Trivy** avant le build Docker garantit qu'aucune image vulnérable n'est publiée dans le registre
- La construction Docker est réservée aux pushs sur `main` (pas les PR) pour économiser les ressources CI

---

### 5.2 Recommandations pour l'Équipe

#### Recommandation 1 — Logs Structurés (JSON) en Production

**Problème actuel :** Les logs de l'API sont en texte libre (`print()`), difficiles à filtrer et à analyser.

**Recommandation :**
```python
import logging
import json

# Configurer un formatter JSON pour production
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        })

# Usage dans app.py
logger = logging.getLogger(__name__)
logger.info("Prediction requested", extra={"temperature": 18.5, "prediction_mw": 52000})
```

**Bénéfice :** Filtrage en temps réel par niveau, intégration native avec ELK Stack (Elasticsearch + Kibana) ou Azure Monitor.

#### Recommandation 2 — Gestion des Secrets via Variables d'Environnement

**Problème actuel :** Les chemins de fichiers modèles et URLs sont codés en dur dans `app.py`.

**Recommandation :**
```python
# Dans app.py — lire depuis les variables d'environnement
import os

MODEL_PATH    = os.getenv("MODEL_PATH", "models/best_model.joblib")
PIPELINE_PATH = os.getenv("PIPELINE_PATH", "models/data_pipeline.joblib")
ODRE_API_KEY  = os.getenv("ODRE_API_KEY")         # Secret — jamais en clair

# Dans Kubernetes
# kubectl create secret generic api-secrets \
#   --from-literal=ODRE_API_KEY="<votre-cle>"
```

**Règle absolue :** Aucun secret (clé API, mot de passe, token) ne doit figurer dans le code source ni dans les fichiers de configuration versionnés. Utiliser **GitHub Secrets** pour CI/CD et **Kubernetes Secrets** pour la production.

#### Recommandation 3 — Tester les Cas Limites et les Valeurs Aberrantes

**Problème actuel :** Les tests actuels ne couvrent pas les valeurs extrêmes.

**Tests manquants à ajouter :**
```python
def test_predict_extreme_temperature_cold():
    """Test avec température polaire (-15°C) — consommation doit augmenter fortement."""
    payload = {"datetime": "2026-01-15T08:00:00", "temperature": -15.0}
    response = client.post("/predict", json=payload)
    assert response.json()["prediction_mw"] > 80000  # Pic hivernal attendu

def test_predict_extreme_temperature_hot():
    """Test avec canicule extrême (42°C) — consommation doit baisser (été)."""
    payload = {"datetime": "2026-08-01T14:00:00", "temperature": 42.0}
    response = client.post("/predict", json=payload)
    assert response.json()["prediction_mw"] > 0  # Doit rester positif

def test_predict_boundary_datetime():
    """Test à minuit — transition journalière."""
    payload = {"datetime": "2026-06-03T00:00:00", "temperature": 15.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
```

#### Recommandation 4 — Implémenter le Versionning Sémantique Strict

**Recommandation :**
```
Chaque merge sur main DOIT être accompagné d'une mise à jour de la version dans :
  1. src/api/app.py  →  version="1.X.Y"
  2. Un tag Git      →  git tag -a v1.X.Y -m "Description"
  3. CHANGELOG.md    →  Documenter les changements

Convention SemVer :
  MAJOR (1.x.x → 2.x.x) : Breaking change dans l'API (/predict schéma modifié)
  MINOR (1.0.x → 1.1.x) : Nouveau endpoint ou feature non-breaking
  PATCH (1.0.0 → 1.0.1) : Bugfix ou mise à jour interne du modèle
```

#### Recommandation 5 — Backup Automatique des Modèles avant Ré-entraînement

**Problème actuel :** `promote_challenger()` écrase `best_model.joblib` sans backup.

**Correctif recommandé dans `retraining_dag.py` :**
```python
def promote_challenger():
    import shutil
    from datetime import datetime
    
    # 1. Créer un backup horodaté avant d'écraser
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    shutil.copy(
        "models/best_model.joblib",
        f"models/backups/best_model_{timestamp}.joblib"
    )
    shutil.copy(
        "models/data_pipeline.joblib",
        f"models/backups/data_pipeline_{timestamp}.joblib"
    )
    
    # 2. Promouvoir le challenger
    shutil.copy("tmp/challenger_model.joblib", "models/best_model.joblib")
    shutil.copy("tmp/challenger_pipeline.joblib", "models/data_pipeline.joblib")
    print(f"Backup créé, challenger promu (timestamp: {timestamp})")
```

#### Recommandation 6 — PersistentVolume pour les Modèles en Production K8s

**Problème actuel :** Les modèles sont dans le système de fichiers éphémère du conteneur.

**Solution K8s :**
```yaml
# Ajouter dans deployment.yaml
volumes:
- name: models-storage
  persistentVolumeClaim:
    claimName: edf-models-pvc  # Créer le PVC séparément

volumeMounts:
- name: models-storage
  mountPath: /app/models        # Les modèles survivent aux redémarrages
```

#### Recommandation 7 — Rate Limiting sur l'API

**Problème actuel :** L'API n'a pas de protection contre les abus (flooding).

**Recommandation :**
```python
# Utiliser slowapi (compatible FastAPI)
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/predict", response_model=PredictResponse)
@limiter.limit("60/minute")   # Max 60 requêtes par minute par IP
async def predict(request: Request, body: PredictRequest):
    ...
```

Ou, au niveau Kubernetes, via un `Ingress` avec annotations NGINX :
```yaml
nginx.ingress.kubernetes.io/limit-rps: "10"
```

#### Recommandation 8 — Monitoring de l'Explainability (SHAP) en Production

**Problème actuel :** Aucune explication des prédictions n'est fournie aux utilisateurs.

**Recommandation :**
```python
import shap

# Calculer les valeurs SHAP à l'inférence (mode rapide, TreeExplainer ou KernelExplainer)
explainer = shap.KernelExplainer(model.predict, X_background_sample)
shap_values = explainer.shap_values(X_input, nsamples=100)

# Ajouter dans PredictResponse :
# "top_features": {"lag_24h": 0.42, "temperature": 0.31, "hour_sin": 0.18}
```

#### Recommandation 9 — Tests d'Intégration de Bout en Bout dans la CI

**Recommandation :** Ajouter dans `ci_cd.yml` un job de smoke test post-build :
```yaml
- name: Run smoke test against built image
  run: |
    docker run -d -p 8000:8000 --name smoke predictor-api:${GITHUB_SHA}
    sleep 15
    STATUS=$(curl -s http://localhost:8000/health | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
    [ "$STATUS" = "ok" ] && echo "Smoke test passed" || (echo "Smoke test FAILED" && exit 1)
    docker stop smoke
```

#### Recommandation 10 — Documenter les Invariants Métier comme Tests

**Recommandation :** Transformer les règles métier en tests automatisés :
```python
def test_prediction_plausibility():
    """Aucune prédiction ne doit être hors des bornes physiques de la consommation française."""
    MIN_CONSUMPTION_MW = 25_000   # Minimum absolu (nuit estivale)
    MAX_CONSUMPTION_MW = 102_000  # Record historique (février 2012)
    
    payload = {"datetime": "2026-06-03T14:00:00", "temperature": 20.0}
    response = client.post("/predict", json=payload)
    pred = response.json()["prediction_mw"]
    
    assert MIN_CONSUMPTION_MW <= pred <= MAX_CONSUMPTION_MW, \
        f"Prédiction aberrante : {pred} MW hors des bornes physiques"
```

#### Recommandation 11 — Stratégie de Branchement Git Structurée

**Recommandation :** Adopter GitFlow ou trunk-based development avec feature flags :

```
main ─────────────────────────────────── (production toujours stable)
  └─ develop ──────────────────────────── (intégration)
        ├─ feature/add-wind-feature ─────
        ├─ feature/rbfn-hypertuning ─────
        └─ hotfix/fix-503-bug ───────────
```

**Règles :**
- Aucun push direct sur `main` — uniquement via Pull Request avec review obligatoire
- La CI/CD doit être verte avant tout merge
- Tags de release SemVer sur chaque merge sur `main`

#### Recommandation 12 — Mise en Place d'un SLO (Service Level Objective) Formalisé

**Recommandation :** Formaliser et monitorer les engagements de service :

```yaml
# SLO à définir et monitorer via Prometheus/Grafana
SLO Disponibilité:
  cible: 99.5% uptime mensuel
  mesure: rate(http_requests_total{http_status!~"5.."}[30d]) / rate(http_requests_total[30d])

SLO Latence:
  cible: P95 < 200ms pour 99.9% des fenêtres de 5 minutes
  mesure: histogram_quantile(0.95, rate(inference_latency_seconds_bucket[5m]))

SLO Précision:
  cible: MAPE < 6% sur 30 jours glissants
  mesure: Calculé lors du ré-entraînement hebdomadaire
```

---

*Document rédigé le 03 juin 2026 — CDPIA MSPR TPRE932 & TPRE942*
*Livrable 2 : Documentation Technique & Runbook d'Exploitation*
*Basé sur le code source opérationnel du projet EDF/RTE Electricity Consumption Predictor*

---
> **Voir aussi :** [Livrable 1 — Dossier de Déploiement & Maintenabilité](file:///C:/Users/USER/.gemini/antigravity/brain/1e5021d6-d49a-4fe7-9504-c69fb7af4a5a/dossier_deploiement_maintenabilite.md)
