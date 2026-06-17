# Dossier de Cadrage & Cahier des Charges du Projet EDF
## Solution de Prédiction de la Consommation Électrique Nationale (EDF / RTE)

**Référentiel RNCP36582 – Blocs de compétences 3 & 4**  
**Promotion 2025-2026 – MSPR TPRE932 & TPRE942**

---

> **Équipe Projet**
>
> | Membre | MSPR 3 (Bloc 3) | MSPR 4 (Bloc 4) |
> |---|---|---|
> | **Noé Wibaut** | Runbook, doc finale & slides | Project framing & planning *(coordinateur)* |
> | **Djamel Chebbah** | Deployment architecture (Docker, API, cloud, CI/CD) | Agile management & tracking |
> | **Paul-Henri Dourneau** | Data & preprocessing (dataset RTE Eco2mix) | Communication, inclusion & slides |
> | **Dorian Marty** | Maintainability & simulation testing | Technical specifications |
> | **Thuy-Trang Nguyen** | Models & training (ANN, Random Forest, KNN, métriques) | Functional specifications |

---

## Sommaire

1. [Cadrage & Planification du Projet](#1-cadrage--planification-du-projet)
   - 1.1 Contexte et enjeux stratégiques
   - 1.2 Objectifs du projet (métier & techniques)
   - 1.3 Étapes de réalisation du SI
   - 1.4 Découpage en tâches et livrables (WBS simplifié)
   - 1.5 Planification macro (Roadmap / Gantt)
   - 1.6 Ressources humaines, techniques et financières mobilisées

2. [Cahier des Charges Fonctionnel & Technique](#2-cahier-des-charges-fonctionnel--technique)
   - 2.1 Besoins utilisateurs (profil des acteurs EDF/RTE, cas d'usage)
   - 2.2 Cahier des charges fonctionnel
   - 2.3 Cahier des charges technique

---

# 1. Cadrage & Planification du Projet

> **Responsable de cette partie (Bloc 4) : Noé Wibaut** – Project framing & planning (roadmap, WBS, jalons, ressources)

---

## 1.1 Contexte et Enjeux Stratégiques

### 1.1.1 Le Système Électrique Français : Un Équilibre Critique en Temps Réel

Le réseau électrique français repose sur un principe physique fondamental : l'électricité produite en courant alternatif ne peut pas être stockée à grande échelle et doit être consommée **à la milliseconde même où elle est produite**. RTE (Réseau de Transport d'Électricité), en tant que gestionnaire unique du réseau de transport en France métropolitaine, porte la responsabilité légale et physique de cet équilibre permanent à **50 Hz**.

Une déviation de la fréquence nominale est le signe immédiat d'un déséquilibre :
- **Si la demande surpasse la production** → la fréquence chute sous 50 Hz → risque d'effondrement du réseau par déclenchement en cascade (**blackout**).
- **Si la production surpasse la demande** → la fréquence grimpe → endommagement des alternateurs et des équipements électroniques industriels.

### 1.1.2 Le Rôle d'EDF : Responsable d'Équilibre

Dans le cadre du marché libéralisé de l'électricité européen, EDF est qualifié de **Responsable d'Équilibre**. À ce titre :
- EDF doit soumettre à RTE des **prévisions de consommation** pour son portefeuille d'abonnés.
- EDF équilibre ces prévisions via ses propres moyens de production ou des **achats sur les marchés de gros (EPEX SPOT)**.
- Tout écart constaté entre la consommation réelle et l'énergie injectée est facturé par RTE sous forme de **pénalités d'écarts**.

### 1.1.3 Impact Économique des Erreurs de Prévision

Les erreurs de prévision ont des conséquences économiques directes et asymétriques :

| Type d'erreur | Cause | Conséquences |
|---|---|---|
| **Sur-estimation** (Ŷ > Y_réel) | Modèle trop pessimiste | Achat inutile d'électricité sur le marché spot · Démarrage de centrales thermiques coûteuses et polluantes · Revente à perte sur le marché d'ajustement |
| **Sous-estimation** (Ŷ < Y_réel) | Modèle trop optimiste | Déficit d'énergie → achat en urgence à prix de crise · Activation des réserves de puissance (très coûteux) · En cas extrême : délestages physiques ou risque de blackout |

**Seuils de criticité retenus pour le projet :**
- 🟢 **Zone Verte** (MAPE < 3 %) : Gestion fluide, coûts d'écarts minimisés.
- 🟡 **Zone Orange** (MAPE 3-5 %) : Activation légère des réserves secondaires, pénalités modérées.
- 🔴 **Zone Rouge** (MAPE > 5 %) : Risque physique sur le réseau (fréquence < 49,8 Hz), coûts de pénalités majeurs, obligation d'activer des contrats d'effacement industriel.

### 1.1.4 La Thermosensibilité : Facteur Dominant de la Demande Française

La France présente une **thermosensibilité parmi les plus élevées d'Europe** en raison de la prédominance historique du chauffage électrique résidentiel. La relation entre température et consommation est ainsi modélisée :

$$f_{\text{thermique}}(T_t) = \max\left(0,\ 15{,}0 - T_t\right) \times 1\,800\ \text{MW}$$

Cela traduit une augmentation de **1 800 MW par degré perdu sous 15 °C**. En hiver rigoureux (T < 0 °C), cela peut représenter un surcroît de consommation supérieur à **25 GW**, soit l'équivalent de 25 réacteurs nucléaires supplémentaires.

---

## 1.2 Objectifs du Projet (Métier & Techniques)

### 1.2.1 Objectifs Métier

| # | Objectif | Indicateur de succès | Priorité |
|---|---|---|---|
| **OM-1** | Fournir des prévisions de charge demi-horaires à horizon J+1 | MAPE < 5 % sur données de test | Critique |
| **OM-2** | Réduire les pénalités d'écart facturées par RTE à EDF | Précision métier ≥ 65 % (±5 %) | Haute |
| **OM-3** | Permettre aux dispatcheurs RTE d'anticiper les décisions d'activation de centrales | Délai de prévision disponible : 3h avant l'heure cible | Haute |
| **OM-4** | Intégrer la solution dans les consoles de supervision existantes de RTE | API REST standardisée, latence < 200 ms | Moyenne |
| **OM-5** | Assurer la transparence et l'explicabilité des prévisions | Disponibilité des valeurs SHAP par prédiction | Moyenne |

### 1.2.2 Objectifs Techniques et Algorithmiques

| # | Objectif | Critère de réussite | Responsable |
|---|---|---|---|
| **OT-1** | Implémenter et comparer 4 familles d'algorithmes de régression | Tableau comparatif R², RMSE, MAPE, Accuracy ±5 % | Thuy-Trang Nguyen |
| **OT-2** | Construire un pipeline de données robuste depuis l'API ODRE/Eco2mix | Pipeline fonctionnel avec fallback sur données simulées | Paul-Henri Dourneau |
| **OT-3** | Industrialiser le modèle champion en API FastAPI conteneurisée | API opérationnelle sur Kubernetes avec /predict, /health, /metrics | Djamel Chebbah |
| **OT-4** | Mettre en œuvre un pipeline CI/CD automatisé | Déclenchement automatique sur chaque PR (GitHub Actions) | Djamel Chebbah |
| **OT-5** | Implémenter un système de monitoring et de détection de drift | Test de Kolmogorov-Smirnov hebdomadaire avec alertes Prometheus | Dorian Marty |
| **OT-6** | Rédiger le runbook d'exploitation et les guides de conduite du changement | Document validé par l'équipe, procédures de rollback < 30 s | Noé Wibaut |

---

## 1.3 Étapes de Réalisation du SI

Le projet est structuré en **5 grandes phases** correspondant au cycle de vie complet d'un système d'information IA industriel :

### Phase 1 – Cadrage & Gouvernance (Heures 0–6)

**Objectif :** Aligner l'ensemble des parties prenantes sur le périmètre, les contraintes et les livrables du projet.

**Activités :**
- Rédaction de la charte de projet et de la matrice RACI
- Définition des personas métiers et des cas d'usage
- Initialisation du Product Backlog Agile (Jira)
- Modélisation budgétaire (TCO) et allocation des ressources
- Mise en place de la charte de collaboration asynchrone interculturelle (9 centres R&D mondiaux EDF)

**Livrables :** Charte de projet · Matrice RACI · Personas · Backlog initial

---

### Phase 2 – Conception & Architecture (Heures 6–12)

**Objectif :** Définir l'architecture technique cible et les spécifications détaillées du pipeline de données et du modèle.

**Activités :**
- Spécification de l'architecture MLOps (API → Docker → Kubernetes → CI/CD)
- Conception du pipeline de feature engineering (encodage cyclique, lags temporels, inertie thermique)
- Sélection des 4 familles d'algorithmes à comparer (Arbre de Décision, Forêt Aléatoire, KNN, RBFN)
- Rédaction des User Stories et critères d'acceptation

**Livrables :** Diagramme d'architecture · Spécifications techniques · User Stories rédigées

---

### Phase 3 – Développement & Test (Heures 12–30)

**Objectif :** Implémenter, entraîner et valider scientifiquement la solution IA et son infrastructure.

**Activités :**
- Développement du pipeline de données ([data_pipeline.py](file:///c:/Users/USER/Documents/MSPR/src/data/data_pipeline.py))
- Entraînement et comparaison des 4 modèles ([train_evaluate.py](file:///c:/Users/USER/Documents/MSPR/src/models/train_evaluate.py))
- Implémentation du RBFN personnalisé ([custom_rbfn.py](file:///c:/Users/USER/Documents/MSPR/src/models/custom_rbfn.py))
- Développement de l'API FastAPI ([app.py](file:///c:/Users/USER/Documents/MSPR/src/api/app.py))
- Dockerisation multi-stage durcie ([Dockerfile](file:///c:/Users/USER/Documents/MSPR/Dockerfile))
- Écriture des manifestes Kubernetes ([k8s/](file:///c:/Users/USER/Documents/MSPR/k8s/))
- Configuration du pipeline CI/CD GitHub Actions
- Écriture des tests unitaires (Pytest, couverture > 80 %)

**Livrables :** Code source · Modèle champion KNN · Image Docker · Manifestes K8s · Pipeline CI/CD

---

### Phase 4 – Déploiement Pilote (Heures 30–36)

**Objectif :** Valider la solution en conditions opérationnelles réelles et mesurer les performances sous charge.

**Activités :**
- Déploiement sur Google Cloud Platform (VM Djamel Chebbah)
- Simulation de charge (Locust) : 100 utilisateurs → 1 000 utilisateurs concurrents
- Validation du pipeline de monitoring (Prometheus/Grafana)
- Configuration du DAG Airflow de ré-entraînement ([retraining_dag.py](file:///c:/Users/USER/Documents/MSPR/src/pipelines/retraining_dag.py))
- Tests de rollback Kubernetes

**Livrables :** Rapport de tests de charge · Dashboard Grafana · DAG Airflow opérationnel

---

### Phase 5 – Généralisation & Documentation Finale (Heures 36–48)

**Objectif :** Formaliser tous les livrables documentaires pour la présentation jury et assurer la transmission aux équipes de production.

**Activités :**
- Rédaction du Runbook d'exploitation ([RUNBOOK.md](file:///c:/Users/USER/Documents/MSPR/RUNBOOK.md))
- Rédaction du plan d'accompagnement au changement
- Préparation des supports de soutenance (Blocs 3 & 4)
- Documentation finale (rapport technique, dossier de cadrage)
- Revue qualité finale de tous les livrables

**Livrables :** Runbook · Plan de conduite du changement · Slides · Rapport technique final · Dossier de cadrage

---

## 1.4 Découpage en Tâches et Livrables (WBS Simplifié)

### Structure WBS à 3 Niveaux

```
Niveau 1 : Projet Predictor EDF/RTE
│
├── Niveau 2 : LOT 1 – Cadrage, Gouvernance & Stratégie Inclusive
│   ├── Niveau 3 : 1.1 Matrice RACI et Cartographie des Acteurs
│   ├── Niveau 3 : 1.2 Personas Métiers et Matrice de Criticité
│   ├── Niveau 3 : 1.3 Planification WBS et Modélisation Budgétaire
│   └── Niveau 3 : 1.4 Charte de Collaboration Asynchrone et Accessibilité WCAG
│
├── Niveau 2 : LOT 2 – Préparation des Données & Modélisation IA
│   ├── Niveau 3 : 2.1 Pipeline d'Ingestion de l'API ODRE et Fallbacks
│   ├── Niveau 3 : 2.2 Feature Engineering (Cyclique, Lags, Rolling)
│   ├── Niveau 3 : 2.3 Développement de la Classe RBFN Personnalisée
│   └── Niveau 3 : 2.4 Entraînement et Comparaison de Performance des 4 Modèles
│
├── Niveau 2 : LOT 3 – Industrialisation, MLOps & Déploiement Cloud
│   ├── Niveau 3 : 3.1 Conception de l'API FastAPI et Instrumentation Prometheus
│   ├── Niveau 3 : 3.2 Dockerisation Multi-stage Durcie (Non-Root)
│   ├── Niveau 3 : 3.3 Manifestes K8s (Deployment, Service, HPA)
│   ├── Niveau 3 : 3.4 Configuration du Pipeline CI/CD GitHub Actions
│   └── Niveau 3 : 3.5 Simulation de Performance avec Locust
│
└── Niveau 2 : LOT 4 – Maintenabilité & Change Management
    ├── Niveau 3 : 4.1 Script de Monitoring de Drift (Kolmogorov-Smirnov)
    ├── Niveau 3 : 4.2 Pipeline Airflow de Ré-entraînement et Promotion Champion
    ├── Niveau 3 : 4.3 Rédaction du Runbook Technique
    └── Niveau 3 : 4.4 BPMN As-Is/To-Be, Explicabilité SHAP et Lean A3
```

### Tableau des Livrables par Lot

| Code WBS | Tâche | Responsable (Bloc 4) | Estimation | Livrable |
|---|---|---|:---:|---|
| **1.1** | Matrice RACI & Cartographie des acteurs | Djamel Chebbah | 2 h | `raci_matrix.md` |
| **1.2** | Personas métiers & matrice de criticité | Thuy-Trang Nguyen | 2 h | `raci_matrix.md` |
| **1.3** | WBS détaillé & modélisation budgétaire | Noé Wibaut | 2 h | `wbs_budget.md` |
| **1.4** | Charte d'inclusion & accessibilité | Paul-Henri Dourneau | 2 h | `inclusion_charter.md` |
| **2.1** | Script d'ingestion API ODRE + fallback | Paul-Henri Dourneau | 3 h | `data_pipeline.py` |
| **2.2** | Feature Engineering temporel & météo | Paul-Henri Dourneau | 4 h | `data_pipeline.py` |
| **2.3** | Réseau RBFN personnalisé (KMeans + gaussiennes) | Thuy-Trang Nguyen | 4 h | `custom_rbfn.py` |
| **2.4** | Entraînement & évaluation comparative 4 modèles | Thuy-Trang Nguyen | 3 h | `train_evaluate.py` + rapport |
| **3.1** | API FastAPI (/predict, /health, /metrics) | Djamel Chebbah | 3 h | `app.py` |
| **3.2** | Dockerfile multi-stage sécurisé | Djamel Chebbah | 2 h | `Dockerfile` |
| **3.3** | Manifestes Kubernetes (Deployment, Service, HPA) | Djamel Chebbah | 2 h | `k8s/*.yaml` |
| **3.4** | Pipeline CI/CD GitHub Actions | Djamel Chebbah | 2 h | `.github/workflows/ci_cd.yml` |
| **3.5** | Tests de charge Locust | Dorian Marty | 2 h | `locust/locustfile.py` |
| **4.1** | Monitoring drift Kolmogorov-Smirnov | Dorian Marty | 2 h | `drift_detector.py` |
| **4.2** | DAG Airflow ré-entraînement Champion/Challenger | Dorian Marty | 3 h | `retraining_dag.py` |
| **4.3** | Runbook & procédures d'urgence | Noé Wibaut | 2 h | `RUNBOOK.md` |
| **4.4** | BPMN, SHAP, Lean A3 & conduite du changement | Noé Wibaut | 3 h | `plan_accompagnement_changement_IA.md` |
| **5.1** | Documentation finale, slides & dossier de cadrage | Noé Wibaut / Paul-Henri Dourneau | 3 h | Documents finaux |
| **TOTAL** | | | **48 h-homme** | |

---

## 1.5 Planification Macro (Roadmap / Gantt)

La planification s'appuie sur une séquence de **2 Sprints Agiles** organisés sur 38 heures effectives de travail d'équipe, avec des jalons (milestones) intermédiaires clairement identifiés.

### Gantt Macro du Projet

```
HEURES PROJET  │  0        6        12       18       24       30       36       42       48
               │  │────────│────────│────────│────────│────────│────────│────────│────────│
               │
LOT 1          │  ████████████ CADRAGE & GOUVERNANCE
Cadrage        │  [RACI][Personas][WBS][Charte inclusive]
               │                         ⬆ JALON J1 : Backlog validé
LOT 2          │           ████████████████████ DATA & MODÉLISATION
Data           │           [Ingestion API ODRE][Feature Engineering]
IA             │                    [RBFN][Entraîn. 4 modèles][Évaluation]
               │                                      ⬆ JALON J2 : Modèle champion sélectionné (KNN, MAPE 4.68%)
LOT 3          │                         ████████████████████ MLOPS & DÉPLOIEMENT
MLOps          │                         [FastAPI][Docker][K8s][CI/CD]
Deploy.        │                                           [Cloud GCP][Load Tests Locust]
               │                                                     ⬆ JALON J3 : API en production validée
LOT 4          │                                    ████████████████████ MAINTENABILITÉ & CHANGE
Monitoring     │                                    [Drift KS][Airflow DAG]
Docs           │                                              [Runbook][BPMN][SHAP][A3]
               │                                                                ⬆ JALON J4 : Livrables finaux
Restitution    │                                                        ████████ SLIDES & SOUTENANCE
               │                                                        [Bloc 3][Bloc 4]
```

### Jalons Clés (Milestones)

| Jalon | Description | Heure projet | Critère de validation |
|:---:|---|:---:|---|
| **J0** | Kick-off projet – Charte signée | H+0 | Réunion de lancement + backlog initial créé |
| **J1** | Backlog validé, architecture décidée | H+6 | RACI approuvé, stories rédigées, architecture documentée |
| **J2** | Modèle champion sélectionné | H+18 | Rapport comparatif des 4 modèles (MAPE KNN = 4,68 %) |
| **J3** | API en production sur GCP | H+30 | Endpoint `/predict` répond · Load test 1 000 users OK |
| **J4** | Livrables finaux validés | H+42 | Runbook + Documentation + Slides finalisés |
| **J5** | Soutenances jury Blocs 3 & 4 | H+48 | Présentation orale 50 min × 2 |

### Sprints Agiles

**Sprint 1 – Fondations Data & IA** (Heures 0 à 18)
- Objectif : Valider l'ingestion des données, le feature engineering, et obtenir les métriques de performance des 4 modèles.
- Vélocité ciblée : **24 Story Points** – Résultat : 24 SP complétés ✅

**Sprint 2 – Industrialisation & Déploiement** (Heures 18 à 38)
- Objectif : Créer l'API FastAPI, la dockeriser, écrire les manifestes Kubernetes, configurer le monitoring et la CI/CD.
- Vélocité ciblée : **26 Story Points** – Résultat : 26 SP complétés ✅

**Burn-down Chart Simulé :**
```
[Reste à Faire en Story Points]
50 | \
40 |  \
30 |   *─────────────── (Fin Sprint 1 – Data/IA OK)
20 |                 \
10 |                  \
 0 +──────────────────* (Fin Sprint 2 – Déploiement & Monitoring OK)
   H0               H18              H38
```
- Vélocité moyenne de l'équipe : **25 SP / sprint**
- Bloqueur résolu : la complexité du RBFN sans librairie tierce a été absorbée en utilisant KMeans natif de scikit-learn.

---

## 1.6 Ressources Humaines, Techniques et Financières Mobilisées

> **Responsable de cette partie (Bloc 4) : Noé Wibaut** – Project framing & planning

### 1.6.1 Ressources Humaines

#### Équipe Projet – Bloc 3 (Industrialisation & Maintenabilité)

| Membre | Rôle Bloc 3 | Responsabilités principales |
|---|---|---|
| **Thuy-Trang Nguyen** | Models & Training | Implémentation ANN/RBFN, Random Forest, KNN ; calcul des métriques (R², RMSE, MAPE, Accuracy ±5%) ; sélection du modèle champion |
| **Paul-Henri Dourneau** | Data & Preprocessing | Dataset RTE Eco2mix (API ODRE), nettoyage, feature engineering (lags, encodage cyclique, inertie thermique) |
| **Djamel Chebbah** | Deployment Architecture | Docker multi-stage, API FastAPI, déploiement Google Cloud Platform, CI/CD GitHub Actions, versioning |
| **Dorian Marty** | Maintainability & Simulation | Monitoring Prometheus, drift KS, ré-entraînement Airflow, logs, tests de charge Locust |
| **Noé Wibaut** | Runbook, Doc & Slides | Documentation technique, runbook d'exploitation, guide utilisateur, slides Bloc 3 |

#### Équipe Projet – Bloc 4 (Management de Projet)

| Membre | Rôle Bloc 4 | Responsabilités principales |
|---|---|---|
| **Thuy-Trang Nguyen** | Functional Specifications | Besoins utilisateurs, use cases, spécification des sorties de prédictions |
| **Noé Wibaut** | Project Framing & Planning | Roadmap, WBS, jalons, allocation des ressources *(coordinateur général)* |
| **Dorian Marty** | Technical Specifications | Architecture technique, pipeline data, contraintes sécurité, ML |
| **Djamel Chebbah** | Agile Management & Tracking | Backlog Jira, gestion des sprints, KPIs, matrice RACI, suivi d'avancement |
| **Paul-Henri Dourneau** | Communication, Inclusion & Slides | Inclusion, collaboration à distance, mise en forme, slides Bloc 4 |

#### Rôles Scrum

| Rôle | Titulaire | Description |
|---|---|---|
| **Product Owner** | Noé Wibaut | Garant du Product Backlog, priorisation des User Stories, validation des critères d'acceptation |
| **Scrum Master** | Djamel Chebbah | Animation des rituels Agile, résolution des bloqueurs, suivi du Burn-down |
| **Développeurs / Data Scientists** | Thuy-Trang Nguyen, Paul-Henri Dourneau, Dorian Marty | Implémentation, tests et validation des incréments |

#### Parties Prenantes Externes

| Acteur | Rôle dans le projet | Mode d'interaction |
|---|---|---|
| **Direction Innovation EDF** | Sponsor – Valide les objectifs métier et les budgets | Revues de sprint (J1, J2, J3) |
| **Dispatcheurs RTE** | Experts métiers – Définissent les seuils de criticité et les cas d'usage | Ateliers de co-conception, personas |
| **Analystes EDF (Trading)** | Utilisateurs finaux de l'API de prédiction | Tests d'acceptation utilisateurs |
| **DSI EDF / RTE** | Intégration dans l'infrastructure de production | Revue d'architecture technique |

### 1.6.2 Ressources Techniques

#### Infrastructure de Développement

| Ressource | Outil / Technologie | Usage |
|---|---|---|
| **Environnement de développement** | Python 3.10+, VS Code, Jupyter | Développement algorithmique et tests |
| **Versioning & CI/CD** | GitHub + GitHub Actions | Contrôle de version, pipeline CI/CD automatisé |
| **Pipeline de données** | Pandas, NumPy, Scikit-Learn, Requests | Ingestion, nettoyage, feature engineering |
| **Entraînement des modèles** | Scikit-Learn (DT, RF, KNN), implémentation custom RBFN | Modélisation et évaluation comparative |
| **API d'inférence** | FastAPI, Uvicorn, Pydantic | Industrialisation du modèle champion |
| **Conteneurisation** | Docker (multi-stage build, non-root) | Encapsulation et sécurisation |
| **Orchestration** | Kubernetes (Deployment, Service, HPA) | Scalabilité et haute disponibilité |
| **Monitoring** | Prometheus, Grafana, SciPy (KS test) | Surveillance opérationnelle et drift |
| **Orchestration MLOps** | Apache Airflow (DAG simulé) | Ré-entraînement automatisé hebdomadaire |
| **Tests de charge** | Locust | Validation des performances sous stress |
| **Sécurité** | Bandit (SAST), Trivy (scan CVE) | Analyse statique et vulnérabilités |
| **Tracking ML** | MLflow (JSON logs) | Traçabilité des métriques d'entraînement |

#### Infrastructure Cloud de Production

| Composant | Service Cloud | Spécifications |
|---|---|---|
| **Cluster Kubernetes** | Google Cloud Platform (VM Djamel) / Azure AKS | 3 pods API – `Standard_B2s` (2 vCPUs, 4 GiB RAM) |
| **Instances GPU (ré-entraînement)** | Azure `Standard_NC6s_v3` | 2h/semaine – à la demande |
| **Stockage artefacts** | Azure Blob Storage | 100 Go, redondance locale |
| **Registre Docker** | Azure Container Registry (Standard) | Images taguées par SHA de commit |
| **Registre de modèles** | MLflow local (JSON) | Métriques, hyperparamètres, version modèle |

### 1.6.3 Ressources Financières (Budget TCO – Coût Total de Possession)

#### Phase Projet (CAPEX)

L'effort total du projet est de **48 heures-homme** réparties sur l'équipe de 5 personnes. Sur la base d'un Taux Journalier Moyen (TJM) de **500 €/jour** (soit 62,50 €/h chargé pour un ingénieur informatique en France) :

$$\text{Coût RH Projet} = 48\ \text{h} \times 62{,}50\ \text{€/h} = 3\,000\ \text{€}$$

#### Phase Exploitation (OPEX – 12 mois de production)

| Poste de dépense | Calcul | Coût annuel |
|---|---|:---:|
| **Cluster AKS (3 pods API)** | 3 × 0,046 €/h × 24h × 365j | **1 208,88 €** |
| **GPU ré-entraînement** | 2 h/sem × 52 sem × 1,50 €/h | **156,00 €** |
| **Stockage Blob Storage** | 100 Go × 0,0184 €/Go/mois × 12 | **22,08 €** |
| **Registre Docker (ACR Standard)** | 0,56 €/j × 365 j | **204,40 €** |
| **MLflow / Grafana Cloud** | Plans Community (open source) | **0 €** |
| **Provision pour risques (10 %)** | Sur total Run | **159,14 €** |
| **Total OPEX annuel** | | **1 750,50 €** |

#### Synthèse Budgétaire (TCO An 1)

| Poste | Phase Projet | Phase Run (annuel) | **Total An 1** |
|---|:---:|:---:|:---:|
| Ressources Humaines | 3 000 € | — | **3 000 €** |
| Calcul Cloud (AKS + GPU) | — | 1 364,88 € | **1 364,88 €** |
| Stockage Cloud | — | 22,08 € | **22,08 €** |
| Registre Docker (ACR) | — | 204,40 € | **204,40 €** |
| Outils MLOps (open source) | — | 0 € | **0 €** |
| Provision risques (10 %) | 300 € | 159,14 € | **459,14 €** |
| **TOTAL** | **3 300 €** | **1 750,50 €** | **5 050,50 €** |

> **Note :** Ce budget est un modèle fictif pédagogique, représentatif d'un déploiement Azure réel à petite échelle. En contexte EDF grand compte, les négociations tarifaires et les contrats Enterprise réduiraient substantiellement le coût Cloud.

---

# 2. Cahier des Charges Fonctionnel & Technique

---

## 2.1 Besoins Utilisateurs (Profil des Acteurs EDF/RTE, Cas d'Usage)

> **Responsable de cette partie (Bloc 4) : Thuy-Trang Nguyen** – Functional specifications (besoins users, use cases, outputs prédictions)

### 2.1.1 Cartographie des Acteurs et Matrice RACI

La matrice RACI ci-dessous structure les responsabilités de chaque acteur sur l'ensemble des activités du projet :

| Activités | Direction Innovation EDF (Sponsor) | Dispatcheurs RTE (Experts métiers) | Scrum Master (Djamel) | Data Scientists / Engineers (Thuy-Trang, Paul-Henri) | Ingénieur MLOps (Dorian, Djamel) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Cadrage & Spécification des besoins** | **A** | **C** | **R** | **C** | **I** |
| **Ingestion & Feature Engineering** | **I** | **I** | **I** | **R/A** | **C** |
| **Entraînement & Validation IA** | **I** | **C** | **I** | **R/A** | **C** |
| **Industrialisation (FastAPI, Docker, K8s)** | **I** | **I** | **I** | **C** | **R/A** |
| **Pipeline CI/CD & Sécurité** | **I** | **I** | **I** | **I** | **R/A** |
| **Monitoring Drift & DAG Airflow** | **I** | **C** | **I** | **C** | **R/A** |
| **Conduite du changement & Formations** | **A** | **R** | **R** | **C** | **C** |

*R : Réalise · A : Approuve · C : Consulté · I : Informé*

### 2.1.2 Personas Métiers

#### Persona 1 : Marc – Dispatcheur National chez RTE

| Attribut | Description |
|---|---|
| **Âge / Expérience** | 45 ans – 15 ans d'expérience en exploitation de réseaux électriques |
| **Organisation** | RTE – Centre National de Supervision (travail en quarts 3×8) |
| **Objectif métier principal** | Maintenir en temps réel l'équilibre offre-demande sur le réseau français à 50 Hz |
| **Besoin clé** | Disposer de prévisions fiables demi-horaires pour planifier l'activation ou l'effacement de capacités de secours (centrales de pointe, importations transfrontalières) |
| **Frustrations actuelles** | ① Manque d'explicabilité des modèles "boîte noire" qui ne justifient pas leurs variations · ② Faux positifs météo déclenchant des démarrages de centrales coûteux et inutiles |
| **Rapport à l'IA** | Exige une interface transparente avec **explicabilité locale** (ex : "Pourquoi la prévision de 18h grimpe de 2 GW alors que le ciel semble dégagé ?") |
| **Contrainte d'usage** | Doit pouvoir **surcharger manuellement** la prédiction si une information terrain exceptionnelle est disponible (grève industrielle, événement non modélisé) |

#### Persona 2 : Léa – Analyste du Mix Énergétique chez EDF

| Attribut | Description |
|---|---|
| **Âge / Expérience** | 29 ans – Diplômée en finance de l'énergie et économie |
| **Organisation** | EDF – Direction Trading & Portfolio Management |
| **Objectif métier principal** | Optimiser les flux d'achats/ventes d'électricité sur les marchés SPOT (EPEX SPOT) à horizon J-1 et intra-journalier |
| **Besoin clé** | Anticiper les volumes de consommation des clients EDF pour minimiser le coût d'écart facturé par RTE |
| **Frustrations actuelles** | ① Manque de flexibilité des prévisions classiques (mauvaise intégration de l'inertie thermique des bâtiments) · ② Temps d'accès trop lents durant les sessions de marché rapides |
| **Rapport à l'IA** | Demande un modèle **performant, scalable, accessible via une API ultra-rapide** (< 200 ms) et sécurisée |
| **Contrainte d'usage** | Nécessite des appels API en temps réel avec des volumes pouvant atteindre 1 000 requêtes simultanées lors des rafraîchissements horaires Eco2mix |

### 2.1.3 Cas d'Usage Principaux

#### UC-01 : Prévision de Consommation Demi-Horaire en Temps Réel

| Attribut | Détail |
|---|---|
| **Acteurs** | Dispatcheur RTE (Marc) / Console de supervision RTE |
| **Déclencheur** | Envoi automatique toutes les 30 minutes par le système de supervision, ou requête manuelle d'un dispatcheur |
| **Précondition** | Le modèle KNN est chargé en mémoire ; l'API est en état `{"status": "ok"}` |
| **Flux nominal** | 1. La console envoie `POST /predict` avec `datetime` et `temperature` (+ lags optionnels) → 2. L'API valide le schéma Pydantic → 3. Le pipeline applique le feature engineering → 4. Le modèle KNN produit une prédiction en MW → 5. La réponse JSON est retournée avec `prediction_mw`, `latency_sec`, `model_used` |
| **Flux alternatif** | Si les lags sont absents : l'API applique des valeurs par défaut intelligentes (55 000 MW) → la prédiction reste valide mais moins précise |
| **Postcondition** | La prédiction est affichée sur la console RTE · La valeur est exportée vers Prometheus (`predicted_consumption_megawatts`) |
| **SLA** | Latence < 200 ms · Taux d'erreur = 0 % |

#### UC-02 : Supervision de la Santé du Système (Monitoring)

| Attribut | Détail |
|---|---|
| **Acteurs** | Ingénieur MLOps (Dorian Marty) / Grafana / Prometheus |
| **Déclencheur** | Polling automatique Prometheus toutes les 15 secondes |
| **Flux nominal** | 1. Prometheus interroge `GET /metrics` → 2. L'API retourne les métriques au format Prometheus (counter requêtes, histogram latence, gauge consommation prédite) → 3. Grafana visualise les dashboards en temps réel |
| **Cas critique** | Si le modèle n'est pas chargé → `GET /health` retourne `{"status": "unhealthy"}` → K8s isole le pod et le redémarre automatiquement |

#### UC-03 : Détection de Drift et Ré-entraînement Automatique

| Attribut | Détail |
|---|---|
| **Acteurs** | Système automatisé (Airflow DAG) / Ingénieur MLOps |
| **Déclencheur** | Programmation hebdomadaire (`@weekly`) ou alerte manuelle de drift |
| **Flux nominal** | 1. Le module KS compare les distributions de température production vs entraînement → 2. Si p-value < 0,05 → alerte ROUGE sur Grafana → 3. Le DAG Airflow déclenche l'extraction des 90 derniers jours → 4. Entraînement du Challenger → 5. Comparaison Champion vs Challenger (MAPE) → 6. Si Challenger < Champion et MAPE ≤ 5 % → promotion en production |

#### UC-04 : Rollback d'Urgence

| Attribut | Détail |
|---|---|
| **Acteurs** | Ingénieur MLOps / Administrateur K8s |
| **Déclencheur** | Anomalie critique détectée après un déploiement (MAPE >> 5 %) |
| **Flux nominal** | `kubectl rollout undo deployment/edf-consumption-predictor-api` → Kubernetes restaure l'image précédente en < 30 secondes |
| **SLA de rollback** | < 30 secondes sans interruption de service (RollingUpdate maxUnavailable: 0) |

---

## 2.2 Cahier des Charges Fonctionnel

> **Responsable de cette partie (Bloc 4) : Thuy-Trang Nguyen** – Functional specifications
> **Co-rédaction :** Dorian Marty (Technical Specifications)

### 2.2.1 User Stories et Critères d'Acceptation

#### EPIC 1 : Acquisition & Feature Engineering (Données)

**US 1.1 – Ingestion automatique de la consommation RTE**

> *En tant qu'Analyste Mix Énergétique (Léa), je veux récupérer automatiquement la consommation électrique nationale depuis l'API publique ODRE afin de disposer d'un historique rafraîchi pour entraîner nos modèles.*

**Critères d'acceptation :**
- [ ] Le script extrait les données nationales au pas demi-horaire (30 min)
- [ ] En cas d'indisponibilité de l'API ODRE (timeout > 5 s), le système bascule automatiquement sur des données synthétiques haute fidélité
- [ ] Les données synthétiques reproduisent les cycles réels (saisonnier, journalier, thermosensibilité) avec une fidélité ≥ 95 % par rapport aux données réelles
- [ ] Le module est testé (Pytest, couverture > 80 %)

**US 1.2 – Feature Engineering Temporel & Climatologique**

> *En tant que Data Scientist, je veux enrichir les données de consommation brute avec des indicateurs thermiques et calendaires afin d'optimiser la pertinence prédictive des algorithmes.*

**Critères d'acceptation :**
- [ ] Encodage cyclique trigonométrique des heures (sin/cos) et des mois (sin/cos)
- [ ] Calcul des lags temporels : t-24h (48 pas), t-48h (96 pas), t-7j (336 pas)
- [ ] Calcul des moyennes mobiles de température : 3h (6 pas), 6h (12 pas)
- [ ] Détection automatique des jours fériés français (bibliothèque `holidays`)
- [ ] StandardScaler appliqué uniquement sur le jeu d'entraînement (pas de fuite de données)

---

#### EPIC 2 : Modélisation Algorithmique

**US 2.1 – Modèles Baselines (Arbre, Forêt, KNN)**

> *En tant que Data Scientist, je veux entraîner trois algorithmes de référence afin de disposer d'une base de comparaison scientifique pour le RBFN.*

**Critères d'acceptation :**
- [ ] Arbre de Décision : `max_depth=8`, critère MSE
- [ ] Forêt Aléatoire : `n_estimators=30`, bagging activé
- [ ] KNN : `k=5`, pondération par l'inverse de la distance
- [ ] Calcul et export de R², RMSE, MAPE, Accuracy ±5 %, temps d'entraînement
- [ ] Métriques tracées dans le registre MLflow (JSON)

**US 2.2 – Réseau RBFN Personnalisé**

> *En tant que Data Scientist, je veux développer un réseau RBF personnalisé (K-Means + gaussiennes + régression Ridge) afin de capturer la non-linéarité thermique.*

**Critères d'acceptation :**
- [ ] Architecture conforme : Couche d'entrée → 30 centres K-Means → activations gaussiennes → régression Ridge (α=0,1)
- [ ] Interface scikit-learn compatible (`fit`, `predict`, `get_params`, `set_params`)
- [ ] Calcul dynamique de γ à partir des distances inter-centroids
- [ ] Évaluation comparative sur le même jeu de test que les 3 autres modèles

**Résultats obtenus (métriques de référence) :**

| Modèle | R² Score | RMSE (MW) | MAPE | Accuracy (±5%) | Temps |
|---|:---:|:---:|:---:|:---:|:---:|
| **Decision Tree** | 0,4712 | 3 617,6 | 5,48 % | 64,42 % | 0,020 s |
| **Random Forest** | 0,5838 | 3 209,2 | 4,87 % | 67,97 % | 0,064 s |
| **KNN ⭐ Champion** | **0,6011** | **3 142,1** | **4,68 %** | **69,48 %** | 0,009 s |
| **RBFN** | -0,3613 | 5 804,2 | 9,19 % | 48,04 % | 1,251 s |

> **Justification du choix KNN :** Le modèle KNeighbors affiche le MAPE le plus faible (4,68 %), une précision métier de 69,48 % et une inférence en moins de 10 ms. Ces caractéristiques en font le candidat idéal pour la mise en production, respectant parfaitement les contraintes SLA de latence (< 200 ms) et le seuil critique de précision (< 5 %).

---

#### EPIC 3 : API & Infrastructure MLOps

**US 3.1 – API d'Inférence Sécurisée (FastAPI)**

> *En tant que Dispatcheur RTE (Marc), je veux envoyer des requêtes JSON sur `/predict` et recevoir instantanément la prévision de charge afin d'automatiser les arbitrages de dispatching.*

**Critères d'acceptation :**
- [ ] Endpoint `POST /predict` validant le schéma d'entrée avec Pydantic (datetime ISO 8601 + température + lags optionnels)
- [ ] Endpoint `GET /health` retournant `{"status": "ok"}` si le modèle est chargé, `{"status": "unhealthy"}` sinon
- [ ] Endpoint `GET /metrics` exposant les métriques Prometheus (counter, histogram, gauge)
- [ ] Latence p95 < 200 ms sous charge nominale (100 utilisateurs)
- [ ] Taux d'erreur HTTP = 0 % en conditions nominales et de crête

**US 3.2 – Conteneurisation & Déploiement (Docker + K8s)**

> *En tant qu'Ingénieur MLOps (Djamel), je veux déployer l'API dans un conteneur sécurisé orchestré par Kubernetes afin de garantir haute disponibilité et scalabilité.*

**Critères d'acceptation :**
- [ ] Dockerfile multi-stage (builder + runner) réduisant la taille de l'image finale de 60 %
- [ ] Exécution sous utilisateur non-root (`appuser`, UID/GID 999)
- [ ] Manifeste Deployment K8s : 3 répliques, stratégie RollingUpdate (`maxUnavailable: 0`)
- [ ] HPA configuré : scale-out automatique si CPU > 70 %, jusqu'à 10 pods maximum
- [ ] Probes Kubernetes : `livenessProbe` et `readinessProbe` sur `/health`

**US 3.3 – Pipeline CI/CD Automatisé**

> *En tant que Développeur MLOps, je veux automatiser la validation du code à chaque pull request afin de prévenir le déploiement de régressions ou de failles de sécurité.*

**Critères d'acceptation :**
- [ ] Pipeline déclenché sur chaque PR vers `main`
- [ ] Étape 1 : Linting & formatage (`black`, `flake8`, `mypy`)
- [ ] Étape 2 : Tests unitaires Pytest (couverture > 80 %)
- [ ] Étape 3 : Scans de sécurité (`Bandit` SAST + `Trivy` CVE)
- [ ] Blocage du merge si l'une des étapes échoue

---

#### EPIC 4 : Maintenabilité & Conduite du Changement

**US 4.1 – Monitoring de Drift et Alertes**

> *En tant qu'Ingénieur MLOps (Dorian), je veux être alerté automatiquement en cas de dérive des données de production afin de déclencher un ré-entraînement avant que les performances ne chutent sous 5 %.*

**Critères d'acceptation :**
- [ ] Test de Kolmogorov-Smirnov hebdomadaire sur la distribution de température (production vs entraînement)
- [ ] Seuil d'alerte : p-value < 0,05 → statut drift ROUGE
- [ ] Alerte publiée sur l'endpoint `/metrics` (Prometheus) → visible sur Grafana
- [ ] Dashboard Grafana avec code couleur accessible (palette ColorBrewer, symboles `✔ ⚠ ✖`)

**US 4.2 – Ré-entraînement Automatique (Airflow)**

> *En tant qu'Ingénieur MLOps, je veux un DAG Airflow hebdomadaire qui ré-entraîne automatiquement un modèle Challenger et le promeut en production si sa performance dépasse le Champion.*

**Critères d'acceptation :**
- [ ] DAG avec 4 tâches séquentielles : Extract → Train Challenger → Evaluate → Promote
- [ ] Promotion uniquement si MAPE Challenger < MAPE Champion ET MAPE Challenger ≤ 5 %
- [ ] Traçabilité complète dans les logs MLflow (JSON)
- [ ] Rollback automatique si la promotion échoue

### 2.2.2 Règles de Gestion Métier

| ID | Règle | Source |
|---|---|---|
| **RG-01** | Une prédiction est considérée acceptable si son écart absolu avec la valeur réelle est ≤ 5 % (MAPE ≤ 5 %) | Seuil de criticité RTE |
| **RG-02** | En dessous de 15 °C, chaque degré de refroidissement supplémentaire induit +1 800 MW de consommation (thermosensibilité) | Modèle physique France |
| **RG-03** | Le modèle Challenger ne peut remplacer le Champion en production que si son MAPE est strictement inférieur au Champion ET inférieur à 5 % | DoD – Règle de promotion |
| **RG-04** | L'API doit retourner une réponse en moins de 200 ms au p95 sous charge nominale (100 utilisateurs concurrents) | SLA opérationnel |
| **RG-05** | Le rollback d'urgence doit être exécutable en moins de 30 secondes sans interruption de service | SLA de maintenance |
| **RG-06** | Aucune donnée nominative ou personnellement identifiable ne doit être ingérée (RGPD) – uniquement des agrégats nationaux | Contrainte légale RGPD |
| **RG-07** | Un drift statistiquement significatif (KS p-value < 0,05) déclenche obligatoirement une alerte sur Grafana | Règle de monitoring |
| **RG-08** | Le ré-entraînement hebdomadaire est planifié pendant les heures creuses nocturnes (00h00 – 05h00) pour minimiser l'empreinte carbone | Règle de sobriété numérique |

### 2.2.3 Attentes Métier Synthétiques

| Dimension | Attente | Indicateur de mesure |
|---|---|---|
| **Précision** | MAPE < 5 % sur l'ensemble du jeu de test | Rapport de performance modèle |
| **Disponibilité** | Uptime API ≥ 99,5 % sur 12 mois | Prometheus (compteur erreurs 5xx) |
| **Latence** | p95 < 200 ms sous charge nominale (100 req simultanées) | Résultats Locust |
| **Scalabilité** | Maintien du SLA latence jusqu'à 1 000 requêtes concurrentes | Tests de crête Locust |
| **Explicabilité** | Valeurs SHAP disponibles pour chaque prédiction significative | Module SHAP intégré |
| **Traçabilité** | Chaque entraînement tracé avec ses métriques, hyperparamètres et version | MLflow JSON logs |
| **Conformité** | Zéro donnée personnelle ingérée, conformité RGPD totale | Audit de données |

---

## 2.3 Cahier des Charges Technique

> **Responsable de cette partie (Bloc 4) : Dorian Marty** – Technical specifications (architecture technique, pipeline data, sécurité, ML)

### 2.3.1 Architecture Technique Cible

#### Vue d'Ensemble de l'Architecture MLOps

```
┌──────────────────────────────────────────────────────────────────────┐
│                    COUCHE D'INGESTION DES DONNÉES                    │
│                                                                      │
│  ┌─────────────────────────────────┐   ┌──────────────────────────┐  │
│  │ API ODRE (Eco2mix RTE)          │   │ Données Synthétiques     │  │
│  │ eco2mix-national-tr             │──▶│ (Fallback haute fidélité)│  │
│  │ Fréquence : 30 min              │   │ data_pipeline.py         │  │
│  └─────────────────────────────────┘   └──────────────────────────┘  │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│               COUCHE DE FEATURE ENGINEERING & MODÉLISATION           │
│                                                                      │
│  ┌──────────────────┐  ┌───────────────────────────────────────────┐ │
│  │ DataPipeline     │  │ Entraînement & Sélection des Modèles       │ │
│  │ · Encodage sin/  │  │ · DecisionTree (max_depth=8)               │ │
│  │   cos (heure,    │  │ · RandomForest (30 estimateurs)            │ │
│  │   mois)          │  │ · KNN (k=5, weights=distance) ⭐ CHAMPION  │ │
│  │ · Lags t-24h,    │  │ · RBFN Custom (KMeans + Ridge)            │ │
│  │   t-48h, t-7j    │  │                                            │ │
│  │ · Roll.Mean 3h,  │  │   Métriques → MLflow JSON                 │ │
│  │   6h temperature │  │   Modèle → models/best_model.joblib        │ │
│  │ · StandardScaler │  │   Pipeline → models/data_pipeline.joblib   │ │
│  └──────────────────┘  └───────────────────────────────────────────┘ │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    COUCHE D'INFÉRENCE (PRODUCTION)                   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │  API FastAPI (src/api/app.py) – Uvicorn – Port 8000          │    │
│  │                                                              │    │
│  │  POST /predict  →  Inférence KNN  →  JSON (MW + latency)    │    │
│  │  GET /health    →  Statut du pod K8s                         │    │
│  │  GET /metrics   →  Format Prometheus                         │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                    │ (Containerisé – Docker)                         │
│                    ▼                                                  │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │  Cluster Kubernetes (GCP / Azure AKS)                        │    │
│  │  · 3 Replicas → RollingUpdate (maxUnavailable: 0)            │    │
│  │  · HPA : scale de 3 à 10 pods si CPU > 70 %                  │    │
│  │  · LoadBalancer Service (port 80 → 8000)                     │    │
│  └──────────────────────────────────────────────────────────────┘    │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐   ┌──────────────────────────────────────┐
│  COUCHE DE MONITORING   │   │  COUCHE CI/CD (GitHub Actions)       │
│                         │   │                                      │
│  Prometheus (scraping   │   │  PR → Lint (Black/Flake8/Mypy)       │
│  /metrics toutes 15s)   │   │  → Tests Pytest (> 80% coverage)     │
│       │                 │   │  → Scan Bandit + Trivy               │
│       ▼                 │   │  → Build Docker → Push ACR            │
│  Grafana Dashboard      │   │  → Deploy K8s (kubectl rollout)      │
│  (Drift, Latence,       │   │                                      │
│   Prédictions)          │   └──────────────────────────────────────┘
└─────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│  COUCHE MLOPS – CYCLE DE VIE DU MODÈLE (Apache Airflow)        │
│                                                                 │
│  @weekly : Extract(90j) → Train Challenger → Eval Champion/     │
│  Challenger → Promote si MAPE_chal < MAPE_champ ≤ 5 %         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3.2 Contraintes d'Architecture

| Contrainte | Exigence | Justification |
|---|---|---|
| **Haute Disponibilité** | Uptime ≥ 99,5 % | SLA critique réseau électrique national |
| **Scalabilité horizontale** | De 3 à 10 pods K8s automatiquement | Pics synchronisés des rafraîchissements Eco2mix |
| **Stateless** | L'API ne doit pas stocker d'état de session | Compatibilité avec le LoadBalancer K8s |
| **Immuabilité des artefacts** | Chaque image Docker est taguée avec le SHA Git | Reproductibilité et rollback garanti |
| **Séparation Build/Run** | Dockerfile multi-stage obligatoire | Réduction de la surface d'attaque (suppression des outils de build) |
| **Non-root** | UID/GID 999 (`appuser`) dans tous les containers | Mitigation du risque d'évasion de container |
| **Stockage des modèles** | Modèles serialisés avec joblib dans `/app/models/` | Chargement rapide au démarrage de l'API |

### 2.3.3 Contraintes de Données

#### Sources de Données

| Source | Type | Fréquence | Format | Accès |
|---|---|---|---|---|
| **ODRE – Eco2mix-national-tr** | Données de consommation électrique | 30 min (temps réel) | JSON via REST API | Public – `https://odre.opendatasoft.com/api/v2/` |
| **Météo-France (Synop)** | Données de température nationale | 30 min / 1h | Intégrée au pipeline (simulation haute fidélité) | Public |
| **Données Synthétiques (fallback)** | Simulation modèle mathématique | Générées à la demande | DataFrame Pandas | Interne au pipeline |

#### Modèle de Données des Features

| Feature | Type | Description | Plage de valeurs |
|---|---|---|---|
| `temperature` | float | Température nationale moyenne (°C) | [-10 ; +40] |
| `hour_sin` | float | Encodage cyclique sinus de l'heure | [-1 ; +1] |
| `hour_cos` | float | Encodage cyclique cosinus de l'heure | [-1 ; +1] |
| `month_sin` | float | Encodage cyclique sinus du mois | [-1 ; +1] |
| `month_cos` | float | Encodage cyclique cosinus du mois | [-1 ; +1] |
| `day_of_week` | int | Jour de la semaine (0=Lundi, 6=Dimanche) | [0 ; 6] |
| `is_weekend` | int | Indicateur week-end | {0, 1} |
| `is_holiday` | int | Indicateur jour férié français | {0, 1} |
| `lag_24h` | float | Consommation 24h avant (MW) | [30 000 ; 90 000] |
| `lag_48h` | float | Consommation 48h avant (MW) | [30 000 ; 90 000] |
| `lag_7d` | float | Consommation 7 jours avant (MW) | [30 000 ; 90 000] |
| `temp_roll_mean_3h` | float | Moyenne glissante température 3h (°C) | [-10 ; +40] |
| `temp_roll_mean_6h` | float | Moyenne glissante température 6h (°C) | [-10 ; +40] |

**Variable cible :**
- `consommation` : Charge électrique nationale prédite en **MW** · Plage observée : [30 000 ; 90 000 MW]

#### Qualité des Données

| Critère | Méthode de traitement |
|---|---|
| **Valeurs manquantes (courte durée)** | Interpolation linéaire sur les créneaux < 3h |
| **Valeurs manquantes (longue durée)** | Imputation par la moyenne du même jour/heure de la semaine précédente |
| **Valeurs aberrantes** | Détection par IQR (1,5× l'intervalle interquartile) → correction par interpolation |
| **Fuite de données (data leakage)** | Séparation chronologique stricte (80/20) – StandardScaler fitté uniquement sur le train |
| **Décalage temporel** | Lag features calculées avec shift() → premières lignes supprimées lors de l'entraînement |

### 2.3.4 Contraintes d'Intégration

#### API – Schéma de Requête/Réponse

**Requête `POST /predict` :**

```json
{
  "datetime": "2026-06-01T18:30:00",
  "temperature": 12.5,
  "lag_24h": 58000.0,
  "lag_48h": 57500.0,
  "lag_7d": 56000.0,
  "temp_roll_mean_3h": 12.1,
  "temp_roll_mean_6h": 11.8
}
```

*Note : les champs `lag_*` et `temp_roll_mean_*` sont optionnels. Par défaut, l'API utilise 55 000 MW et `temperature` respectivement.*

**Réponse `200 OK` :**

```json
{
  "datetime": "2026-06-01 18:30:00",
  "prediction_mw": 62340.5,
  "status": "success",
  "model_used": "KNeighborsRegressor",
  "latency_sec": 0.0089
}
```

**Codes d'erreur standardisés :**

| Code HTTP | Signification | Action corrective |
|:---:|---|---|
| `200` | Prédiction réussie | — |
| `400` | Format datetime invalide | Vérifier le format ISO 8601 |
| `503` | Modèle non initialisé | Vérifier `GET /health` + logs du pod |
| `500` | Erreur d'inférence interne | Consulter le Runbook – Section "Incident B" |

#### Intégration Prometheus/Grafana

Les métriques exposées sur `GET /metrics` :

| Métrique Prometheus | Type | Description |
|---|---|---|
| `http_requests_total` | Counter | Nombre total de requêtes HTTP par méthode, endpoint, status |
| `inference_latency_seconds` | Histogram | Temps de réponse de `/predict` (buckets : 1ms → 5s) |
| `predicted_consumption_megawatts` | Gauge | Dernière valeur de charge prédite en MW |

### 2.3.5 Contraintes de Performance

| Scénario | Métrique | Seuil |
|---|---|---|
| **Charge nominale** (100 users) | Latence moyenne | < 25 ms |
| **Charge nominale** (100 users) | Latence p95 | < 50 ms |
| **Charge nominale** (100 users) | Taux d'erreur | 0,0 % |
| **Charge de crête** (1 000 users) | Latence p95 | < 200 ms |
| **Charge de crête** (1 000 users) | Débit maintenu | ≥ 400 req/s |
| **Charge de crête** (1 000 users) | Taux d'erreur | 0,0 % |
| **Inférence unitaire** | Temps modèle KNN | < 10 ms |
| **Démarrage de l'API** | Chargement du modèle | < 5 s |

**Résultats validés par les tests Locust :**

| Scénario | Résultat Locust | Conformité |
|---|---|:---:|
| 100 users concurrents | 45 req/s · latence moy. 12 ms · p95 = 35 ms · 0 % erreur | ✅ |
| 1 000 users concurrents | 420 req/s · latence moy. 68 ms · p95 = 185 ms · 0 % erreur | ✅ |

### 2.3.6 Contraintes de Sécurité

| Domaine | Mesure Implémentée | Standard de référence |
|---|---|---|
| **Conteneur non-root** | `USER appuser` (UID 999) dans Dockerfile · `runAsNonRoot: true` dans K8s | CIS Docker Benchmark |
| **Image minimale** | Multi-stage build : seuls les packages d'inférence sont dans l'image finale | NIST SP 800-190 |
| **Capabilities** | `capabilities: drop: [ALL]` dans le securityContext K8s | Principe du moindre privilège |
| **Filesystem** | `readOnlyRootFilesystem: false` (requis pour modèles) · Dossier `/app/models` isolé | CIS K8s Benchmark |
| **Analyse statique (SAST)** | `Bandit` : zéro faille de criticité moyenne ou haute | OWASP ASVS |
| **Analyse vulnérabilités (CVE)** | `Trivy` : zéro CVE critique ou élevée sur les dépendances + image Docker | NVD / CVE Database |
| **Aucune donnée personnelle** | Pipeline n'ingère que des agrégats nationaux (consommation MW à l'échelle nationale) | RGPD Art. 5 (minimisation) |
| **Secrets** | Aucun secret en dur dans le code · Variables d'environnement K8s Secrets | OWASP Top 10 A2 |
| **Élévation de privilèges** | `allowPrivilegeEscalation: false` dans le securityContext | CIS Docker Benchmark |

### 2.3.7 Architecture du Système de Monitoring et de Drift

#### Modèle Mathématique du Drift (Test de Kolmogorov-Smirnov)

La détection de dérive repose sur le **test bilatéral de Kolmogorov-Smirnov à deux échantillons** appliqué à la variable de température :

Soit $F_{\text{ref}}(x)$ la fonction de répartition empirique de la température dans le jeu d'entraînement :
$$F_{\text{ref}}(x) = \frac{1}{N_{\text{ref}}} \sum_{i=1}^{N_{\text{ref}}} \mathbb{I}(X_{i,\text{ref}} \le x)$$

Soit $F_{\text{prod}}(x)$ la fonction de répartition empirique calculée sur les températures de production de la semaine écoulée :
$$F_{\text{prod}}(x) = \frac{1}{N_{\text{prod}}} \sum_{i=1}^{N_{\text{prod}}} \mathbb{I}(X_{i,\text{prod}} \le x)$$

La statistique $D$ mesure la divergence maximale entre les deux distributions :
$$D = \sup_x \left| F_{\text{ref}}(x) - F_{\text{prod}}(x) \right|$$

**Règle de décision :** Si la p-value associée à $D$ est inférieure à $\alpha = 0,05$ → rejet de $H_0$ → **drift statistiquement significatif détecté** → alerte ROUGE publiée sur Prometheus.

#### Niveaux d'Alerte Grafana

| Niveau | Condition | Couleur | Symbole | Action |
|---|---|:---:|:---:|---|
| **Nominal** | MAPE < 3 % · Pas de drift | 🔵 Bleu | `✔` | Surveillance passive |
| **Vigilance** | 3 % ≤ MAPE ≤ 5 % **OU** drift KS détecté | 🟠 Orange | `⚠` | Surveillance active · Planifier ré-entraînement |
| **Critique** | MAPE > 5 % **OU** drift sévère | 🔴 Rouge | `✖` | Déclencher immédiatement le DAG Airflow · Envisager rollback |

*Note : les palettes respectent les normes WCAG 2.1 et ColorBrewer pour les utilisateurs daltoniens (deutéranopie, protanopie).*

### 2.3.8 Processus de Ré-entraînement MLOps (DAG Airflow)

Le cycle de vie du modèle est géré par un **DAG Apache Airflow** planifié hebdomadairement :

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│ Task 1          │───▶│ Task 2          │───▶│ Task 3             │───▶│ Task 4 (Cond.)  │
│ extract_and_    │    │ train_          │    │ evaluate_and_      │    │ promote/reject  │
│ prepare_data    │    │ challenger      │    │ compare            │    │ challenger      │
│                 │    │                 │    │                    │    │                 │
│ · 90j de        │    │ · KNN Challen.  │    │ · Champion MAPE    │    │ Si MAPE_chal <  │
│   données RTE   │    │ · joblib export │    │ · Challenger MAPE  │    │ MAPE_champ ET   │
│ · Parquet tmp/  │    │ · Pipeline      │    │ · Test 15 derniers │    │ ≤ 5%            │
│                 │    │   export        │    │   jours            │    │ → copie vers    │
│                 │    │                 │    │                    │    │   models/       │
└─────────────────┘    └─────────────────┘    └─────────────────────┘    └─────────────────┘
@weekly · 00h00 · email_on_failure: mlops-alerts@edf.fr · retries: 2
```

### 2.3.9 Stratégie de Gestion des Incidents et Rollback

#### Arbre de Résolution des Incidents Types

| Incident | Symptôme | Diagnostic | Action corrective |
|---|---|---|---|
| **OOMKilled** | Pod K8s redémarré avec `OOMKilled` | Mémoire insuffisante (`kubectl describe pod`) | Augmenter `limits.memory` dans `deployment.yaml` (256Mi → 512Mi) |
| **API Unhealthy** | `/health` retourne `{"status": "unhealthy"}` | Modèle `.joblib` absent ou corrompu | Ré-initialiser le pipeline : `kubectl exec ... python -c "from src.models.train_evaluate import main; main()"` |
| **Drift ROUGE** | Grafana alerte drift KS p-value < 0,05 | Distribution température dérivée | Déclencher manuellement le DAG Airflow : `airflow dags trigger edf_consumption_predictor_retraining` |
| **MAPE > 5 %** | Dégradation confirmée en production | Modèle obsolète ou donnée anormale | 1. Vérifier les données en entrée · 2. Déclencher ré-entraînement · 3. En cas d'échec → rollback |
| **Déploiement défaillant** | Nouveau pod ne passe pas la `readinessProbe` | Image corrompue ou régression code | Rollback immédiat : `kubectl rollout undo deployment/edf-consumption-predictor-api` |

#### Procédure de Rollback (< 30 secondes)

```bash
# 1. Vérifier l'historique des déploiements
kubectl rollout history deployment/edf-consumption-predictor-api -n edf-rte-production

# 2. Revenir à la version précédente stable
kubectl rollout undo deployment/edf-consumption-predictor-api -n edf-rte-production

# 3. Confirmer le statut du rollback
kubectl rollout status deployment/edf-consumption-predictor-api -n edf-rte-production

# 4. Vérifier la santé de l'API
curl https://api.edf-rte.internal/health
```

### 2.3.10 Conformité et Accessibilité

#### Conformité RGPD

| Exigence RGPD | Implémentation |
|---|---|
| **Minimisation des données** | Seuls des agrégats nationaux en MW (aucune donnée individuelle) |
| **Finalité déterminée** | Prévision de charge électrique nationale à vocation opérationnelle exclusive |
| **Sécurité des traitements** | API sécurisée (non-root, scans CVE, réseau K8s isolé) |
| **Droit à l'effacement** | N/A – Aucune donnée personnelle collectée |
| **Registre des traitements** | Modèle documenté dans le registre MLflow avec type de données, finalité et responsable |

#### Accessibilité Numérique (WCAG 2.1 niveau AA)

| Profil de handicap | Mesure implémentée |
|---|---|
| **Daltonisme** (deutéranopie, protanopie) | Palette ColorBrewer bleu/orange (non rouge/vert) sur tous les dashboards Grafana · Symboles textuels `✔ ⚠ ✖` |
| **Déficience visuelle** | Contraste texte minimum 4,5:1 sur les interfaces web (WCAG 2.1 AA) |
| **Neuroatypies** (TDAH, Autisme) | Décomposition des tâches en sous-étapes ≤ 4h (Goblin.tools) · Documentation sans blocs de texte denses · Schémas Mermaid épurés |
| **Déficience auditive** | Sous-titrage automatique Teams Live Captions · Enregistrements vidéo systématiques des réunions et démos de sprint |

#### Collaboration Internationale (9 Centres R&D EDF)

| Centre | Fuseau horaire | Fenêtre commune |
|---|---|---|
| France (Paris) | CET (UTC+1/+2) | **14h00 – 16h00** |
| Chine (Pékin) | CST (UTC+8) | 20h00 – 22h00 |
| États-Unis (New York) | EST (UTC-5/-4) | 08h00 – 10h00 |
| Royaume-Uni (Londres) | GMT (UTC+0/+1) | 13h00 – 15h00 |
| Allemagne (Munich) | CET (UTC+1/+2) | 14h00 – 16h00 |
| Italie (Rome) | CET (UTC+1/+2) | 14h00 – 16h00 |

**Règles de communication asynchrone :**
- Toute décision technique est documentée en **anglais technique** sur Git/Confluence dans les 24h suivant la réunion.
- Canaux Slack/Teams dédiés par domaine : `#data-pipeline` · `#model-training` · `#mlops-k8s` · `#monitoring-alerts`.
- Aucune décision bloquante ne peut être prise sans que tous les membres disposent d'un délai de réponse de 24h minimum.

---

## Conclusion

Ce dossier de cadrage et cahier des charges formalise l'ensemble des exigences fonctionnelles et techniques du projet **EDF/RTE de prédiction de la consommation électrique nationale**. Il constitue le document de référence pour les deux soutenances jury (Bloc 3 & Bloc 4) et atteste de la rigueur méthodologique de l'équipe dans les domaines suivants :

### Synthèse des Engagements

| Dimension | Engagement | Résultat validé |
|---|---|:---:|
| **Précision IA** | MAPE < 5 % (seuil critique réseau) | ✅ KNN : MAPE = 4,68 % |
| **Industrialisation** | API FastAPI conteneurisée K8s | ✅ Déployée sur GCP |
| **Performance** | Latence p95 < 200 ms sous 1 000 users | ✅ 185 ms mesuré (Locust) |
| **Sécurité** | Zéro CVE critique, non-root | ✅ Bandit + Trivy OK |
| **Maintenabilité** | Détection drift + ré-entraînement auto | ✅ KS + Airflow DAG |
| **CI/CD** | Pipeline automatisé sur chaque PR | ✅ GitHub Actions |
| **Accessibilité** | WCAG 2.1 AA | ✅ ColorBrewer + symboles |
| **Conformité RGPD** | Zéro donnée personnelle | ✅ Agrégats nationaux uniquement |

### Équipe et Responsabilités Finales

| Membre | Contribution Bloc 3 | Contribution Bloc 4 |
|---|---|---|
| **Noé Wibaut** | Runbook · Documentation finale · Slides Bloc 3 | **Coordinateur** · Project framing & planning · WBS · Roadmap |
| **Djamel Chebbah** | Architecture déploiement · Docker · GCP · CI/CD | Agile management · Suivi sprints · Backlog Jira · KPIs |
| **Paul-Henri Dourneau** | Data & preprocessing · API ODRE · Feature engineering | Communication · Inclusion · Slides Bloc 4 |
| **Dorian Marty** | Monitoring · Drift KS · Airflow · Tests Locust | Spécifications techniques · Architecture · Sécurité · ML |
| **Thuy-Trang Nguyen** | Models & training · RBFN · Comparaison 4 modèles | Spécifications fonctionnelles · Use cases · Personas |

---

*Document rédigé dans le cadre de la MSPR TPRE932 & TPRE942 – Référentiel RNCP36582 – Promotion 2025-2026.*  
*Date de rédaction : Juin 2026*
