# Dossier de Pilotage Agile & Suivi du Projet
## Solution de Prédiction de la Consommation Électrique Nationale (EDF / RTE)

**Référentiel RNCP36582 – Blocs de compétences 3 & 4**  
**Promotion 2025-2026 – MSPR TPRE932 & TPRE942**

---

> **Équipe Projet – Attribution des rôles**
>
> | Membre | Rôle Bloc 3 | Rôle Bloc 4 |
> |---|---|---|
> | **Noé Wibaut** | Runbook, doc finale & slides | Project framing & planning *(coordinateur)* |
> | **Djamel Chebbah** | Deployment architecture | **Agile management & tracking** *(Scrum Master)* |
> | **Paul-Henri Dourneau** | Data & preprocessing | Communication, inclusion & slides |
> | **Dorian Marty** | Maintainability & simulation | Technical specifications |
> | **Thuy-Trang Nguyen** | Models & training | Functional specifications |

---

## Sommaire

1. [Organisation Agile du Projet](#1-organisation-agile-du-projet)
   - 1.1 Méthode choisie et justification
   - 1.2 Rôles et responsabilités
   - 1.3 Backlog produit (Épics & User Stories priorisées)
   - 1.4 Déroulement des itérations

2. [Tableaux de Bord de Suivi de Projet](#2-tableaux-de-bord-de-suivi-de-projet)
   - 2.1 Liste des KPI projet
   - 2.2 Maquette de tableau de bord
   - 2.3 Utilisation des indicateurs pour anticiper et corriger les écarts

3. [Pilotage des Prestataires & du SI Existant](#3-pilotage-des-prestataires--du-si-existant)
   - 3.1 Cartographie des prestataires et systèmes connectés
   - 3.2 Rôles & responsabilités (RACI)
   - 3.3 Modalités de pilotage

---

# 1. Organisation Agile du Projet

> **Responsable de cette partie (Bloc 4) : Djamel Chebbah** – Agile management & tracking (backlog, sprints, KPIs, RACI, suivi)

---

## 1.1 Méthode Choisie et Justification

### 1.1.1 Choix de la Méthode : Scrum Adapté

L'équipe projet a retenu le cadre **Scrum** comme méthode de pilotage principale, avec des adaptations légères tenant compte du contexte spécifique du projet (contraintes temporelles, dispersion géographique, nature hybride data/MLOps).

#### Pourquoi Scrum et pas Kanban ou SAFe ?

| Critère d'évaluation | Scrum ✅ | Kanban | SAFe |
|---|:---:|:---:|:---:|
| Cadence itérative adaptée au délai projet (38h) | ✅ Sprints courts | ❌ Flux continu peu structurant | ❌ Trop lourd pour 5 personnes |
| Visibilité sur l'avancement et la vélocité | ✅ Burn-down chart | ⚠️ Throughput difficile à lire | ✅ |
| Gestion des dépendances data → IA → déploiement | ✅ Sprints séquentiels | ❌ Risque de silos | ✅ |
| Rôles clairs sans overhead organisationnel | ✅ 3 rôles simples | ❌ Pas de rôle défini | ❌ Trop de rôles |
| Adapté à une équipe de 5 personnes | ✅ | ✅ | ❌ Conçu pour > 50 pers. |
| Rituels légers pour collaboration asynchrone | ✅ (Daily 15 min) | ⚠️ | ❌ |

#### Adaptations Spécifiques au Contexte EDF/RTE

Le Scrum « académique » a été adapté sur deux points pour coller à la réalité opérationnelle :

**1. Sprints raccourcis à durée variable :**
Au lieu de sprints fixes de 2 semaines, les sprints sont calés sur les blocs de compétences (Bloc 3 = Sprint 1 · Bloc 4 = Sprint 2), permettant une livraison distincte et évaluable par les jurys.

**2. Cérémonies asynchrones :**
Le Daily Scrum traditionnel (15 min en présentiel) est remplacé par un **standup écrit asynchrone** sur le canal Slack `#daily-standup`. Chaque membre répond avant 10h à 3 questions :
- *Qu'ai-je terminé hier ?*
- *Que vais-je faire aujourd'hui ?*
- *Ai-je un bloqueur ?*

Cette adaptation est rendue nécessaire par la dispersion des 9 centres R&D mondiaux d'EDF (Paris, Pékin, New York, Londres, Munich, Rome) et les fuseaux horaires incompatibles avec un daily synchrone quotidien.

#### Positionnement sur le Spectre Agile

```
Traditionnel ◄────────────────────────────────────────► Agile pur
   (Cascade)    Cycle en V    SAFe    SCRUM ✅    XP    Lean Startup
                                       ↑
                               Notre positionnement :
                               Scrum avec adaptations
                               asynchrones (Async-First)
```

### 1.1.2 Les Valeurs Scrum Appliquées au Projet

| Valeur Scrum | Application concrète dans le projet |
|---|---|
| **Courage** | Décision de rejeter le RBFN en production malgré l'effort de 4h, en faveur du KNN plus performant |
| **Focus** | Sprints avec objectif unique et mesurable (Sprint 1 : modèle champion · Sprint 2 : API en production) |
| **Engagement** | DoD appliquée sans exception : aucun code fusionné sans review + tests Pytest > 80 % |
| **Respect** | Charte de collaboration inclusive (WCAG 2.1, fuseaux horaires, neuroatypies) |
| **Transparence** | Burn-down chart partagé en temps réel sur Jira · MLflow traceable par tous |

---

## 1.2 Rôles et Responsabilités

### 1.2.1 Les Trois Rôles Scrum

#### Product Owner – Noé Wibaut

| Attribut | Détail |
|---|---|
| **Mission principale** | Garant de la valeur métier du produit. Représente les intérêts des utilisateurs finaux (Dispatcheurs RTE, Analystes EDF) auprès de l'équipe de développement. |
| **Responsabilités clés** | ① Définir, prioriser et maintenir le Product Backlog · ② Rédiger les User Stories avec les critères d'acceptation · ③ Valider les incréments lors des Sprint Reviews · ④ Arbitrer les compromis entre fonctionnalité et délai |
| **Autorité** | Seul décisionnaire sur la priorisation du Backlog. L'équipe ne peut pas modifier les priorités sans accord PO. |
| **Disponibilité** | Disponible quotidiennement pour lever les ambiguïtés sur les US pendant les sprints |
| **KPI de suivi** | Taux d'US validées à la Sprint Review · Nombre de changements de priorité en cours de sprint |

#### Scrum Master – Djamel Chebbah

| Attribut | Détail |
|---|---|
| **Mission principale** | Facilitateur et coach de l'équipe. Garant du respect des pratiques Scrum et de la suppression des obstacles (impediments). |
| **Responsabilités clés** | ① Animer les cérémonies Scrum (Planning, Daily, Review, Rétrospective) · ② Identifier et résoudre les bloqueurs dans les 24h · ③ Protéger l'équipe des interruptions extérieures en cours de sprint · ④ Suivre et publier les KPIs d'agilité |
| **Ce que le Scrum Master N'est PAS** | Chef de projet hiérarchique · Manager de l'équipe · Décisionnaire sur le contenu |
| **Outils utilisés** | Jira (tableau Kanban du sprint) · Slack (canal `#scrum-master-log`) · Burn-down chart Jira |
| **KPI de suivi** | Nombre de bloqueurs résolus / signalés · Vélocité sprint-sur-sprint · Satisfaction d'équipe (rétrospective) |

#### Équipe de Développement (Dev/Data) – Thuy-Trang, Paul-Henri, Dorian

| Membre | Spécialité principale | Capacité sprint |
|---|---|:---:|
| **Thuy-Trang Nguyen** | Data Science & Modélisation IA (RBFN, KNN, RF, métriques) | 12 SP |
| **Paul-Henri Dourneau** | Data Engineering (ingestion API ODRE, feature engineering, prétraitement) | 10 SP |
| **Dorian Marty** | MLOps & Tests (monitoring, drift, Locust, Airflow, maintainabilité) | 12 SP |

**Principes de l'équipe de développement :**
- Auto-organisée : l'équipe décide comment accomplir le travail, pas le Scrum Master.
- Cross-fonctionnelle : chaque membre peut contribuer hors de sa spécialité principale si nécessaire.
- Responsable collectivement : l'incrément est livré par l'équipe, pas par un individu.

### 1.2.2 Les Rôles Métier Complémentaires

Au-delà des 3 rôles Scrum classiques, le contexte industriel EDF/RTE impose des rôles supplémentaires :

| Rôle | Titulaire | Interactions avec l'équipe |
|---|---|---|
| **Référent Métier RTE** | Marc (Dispatcheur National, Persona 1) | Valide les cas d'usage · Participe aux Sprint Reviews · Définit les seuils de criticité (MAPE) |
| **Référent Métier EDF** | Léa (Analyste Mix Énergétique, Persona 2) | Valide les SLA de latence et les formats de réponse API · Tests d'acceptation utilisateurs |
| **Sponsor Projet** | Direction Innovation EDF | Approuve les budgets · Reçoit les rapports d'avancement (vue Sponsor) |
| **Référent Sécurité SI** | DSI EDF / RTE | Valide l'architecture de sécurité (conteneurs, scans Trivy, conformité RGPD) |
| **Référent Cloud** | Équipe Infrastructure GCP/Azure | Support déploiement Kubernetes · SLA de disponibilité Cloud |

### 1.2.3 Matrice de Responsabilités Scrum (RASCI Agile)

| Cérémonie / Activité | PO (Noé) | SM (Djamel) | Équipe (Thuy-Trang, Paul-Henri, Dorian) | Référent Métier | Sponsor |
|---|:---:|:---:|:---:|:---:|:---:|
| **Sprint Planning** | A | R | R | C | I |
| **Daily Standup** | I | R | R | — | — |
| **Développement des US** | C | — | R/A | C | — |
| **Sprint Review** | A | R | R | R | C |
| **Rétrospective** | R | R | R | — | — |
| **Backlog Refinement** | R/A | C | C | C | — |
| **Validation des incrément** | A | — | R | C | — |
| **Reporting Sponsor** | C | R | — | — | A |

*R : Réalise · A : Approuve · S : Supporte · C : Consulté · I : Informé*

---

## 1.3 Backlog Produit (Épics & User Stories Priorisées)

### 1.3.1 Épics et leur Priorité (MoSCoW)

| ID Épic | Intitulé | Priorité MoSCoW | Bloc | Valeur métier |
|---|---|:---:|:---:|---|
| **EPIC-01** | Acquisition & Feature Engineering (Données) | **Must Have** | 3 | Fondation de tout le système prédictif |
| **EPIC-02** | Modélisation Algorithmique (4 modèles + RBFN) | **Must Have** | 3 | Cœur de la valeur IA du projet |
| **EPIC-03** | API & Infrastructure MLOps (FastAPI + K8s) | **Must Have** | 3 | Industrialisation et accessibilité |
| **EPIC-04** | Maintenabilité & Cycle de Vie Modèle | **Should Have** | 3 | Pérennité en production |
| **EPIC-05** | Spécifications Fonctionnelles & Use Cases | **Must Have** | 4 | Alignement métier (Bloc 4) |
| **EPIC-06** | Cadrage Projet & Gouvernance Agile | **Must Have** | 4 | Pilotage et planification (Bloc 4) |
| **EPIC-07** | Communication & Inclusion Internationale | **Should Have** | 4 | Conformité WCAG, collaboration |
| **EPIC-08** | Conduite du Changement & Explicabilité IA | **Could Have** | 4 | Adoption par les utilisateurs finaux |

### 1.3.2 Backlog Produit Complet – User Stories Priorisées

Le tableau ci-dessous présente l'intégralité du Product Backlog, trié par priorité décroissante et accompagné des Story Points (estimés en Planning Poker) :

---

#### 🔴 SPRINT 1 – Fondations Data & IA (Heures 0 à 18) – Priorité HAUTE

**US-01 · EPIC-01 · 5 SP**
> *En tant qu'Analyste Mix Énergétique (Léa), je veux que le système récupère automatiquement les données de consommation électrique nationale depuis l'API ODRE afin d'alimenter nos modèles de prévision avec des données réelles.*

| Critères d'acceptation | Statut |
|---|:---:|
| Le module `DataPipeline.fetch_realtime_data()` interroge l'API ODRE (endpoint `eco2mix-national-tr`) | ✅ |
| En cas de timeout > 5 s ou erreur réseau, le fallback synthétique se déclenche automatiquement | ✅ |
| Les données retournées contiennent les colonnes `datetime`, `consommation` (MW), `temperature` (°C) | ✅ |
| Tests Pytest couvrant le cas nominal et le cas de fallback (couverture ≥ 80 %) | ✅ |
| **Responsable :** Paul-Henri Dourneau | |

---

**US-02 · EPIC-01 · 5 SP**
> *En tant que Data Scientist, je veux enrichir les données brutes avec des variables temporelles cycliques, des lags et des moyennes mobiles de température afin d'optimiser le pouvoir prédictif des algorithmes.*

| Critères d'acceptation | Statut |
|---|:---:|
| Encodage cyclique trigonométrique : `hour_sin`, `hour_cos`, `month_sin`, `month_cos` | ✅ |
| Lags temporels calculés : `lag_24h` (48 pas), `lag_48h` (96 pas), `lag_7d` (336 pas) | ✅ |
| Moyennes mobiles de température : `temp_roll_mean_3h` (6 pas), `temp_roll_mean_6h` (12 pas) | ✅ |
| `StandardScaler` fitté exclusivement sur le jeu d'entraînement (pas de data leakage) | ✅ |
| Indicateur `is_holiday` via la bibliothèque `holidays` (jours fériés français) | ✅ |
| **Responsable :** Paul-Henri Dourneau | |

---

**US-03 · EPIC-02 · 3 SP**
> *En tant que Data Scientist, je veux entraîner un Arbre de Décision et une Forêt Aléatoire et calculer leurs métriques afin de disposer de références de performance.*

| Critères d'acceptation | Statut |
|---|:---:|
| DecisionTreeRegressor : `max_depth=8`, critère MSE | ✅ |
| RandomForestRegressor : `n_estimators=30`, bagging activé | ✅ |
| Calcul de R², RMSE (MW), MAPE (%), Accuracy ±5 %, temps d'entraînement | ✅ |
| Métriques exportées vers le fichier de logs MLflow (JSON) | ✅ |
| **Responsable :** Thuy-Trang Nguyen | |

---

**US-04 · EPIC-02 · 3 SP**
> *En tant que Data Scientist, je veux entraîner un modèle KNN pondéré et le comparer aux modèles baseline afin de sélectionner le meilleur candidat pour la production.*

| Critères d'acceptation | Statut |
|---|:---:|
| KNeighborsRegressor : `n_neighbors=5`, `weights='distance'` | ✅ |
| Métriques identiques aux autres modèles (R², RMSE, MAPE, Accuracy, temps) | ✅ |
| KNN sélectionné comme champion si MAPE < 5 % et meilleur que les alternatives | ✅ |
| **Résultat :** MAPE = 4,68 % · Accuracy = 69,48 % · Temps = 0,009 s | ✅ |
| **Responsable :** Thuy-Trang Nguyen | |

---

**US-05 · EPIC-02 · 8 SP** *(tâche complexe, ticketée sur 2 sous-tâches ≤ 4h)*
> *En tant que Data Scientist, je veux développer un réseau RBFN personnalisé (K-Means + gaussiennes + régression Ridge) et l'évaluer sur le même benchmark afin de capturer la non-linéarité thermique et comparer son apport.*

| Critères d'acceptation | Statut |
|---|:---:|
| Architecture 3 couches : entrée D → 30 centres K-Means → régression Ridge (α=0,1) | ✅ |
| Interface scikit-learn compatible : `fit()`, `predict()`, `get_params()`, `set_params()` | ✅ |
| Calcul dynamique de γ à partir des distances inter-centroids | ✅ |
| Évaluation sur le même jeu de test 80/20 que les autres modèles | ✅ |
| **Résultat :** R² = -0,36 → RBFN écarté de la production (justification documentée) | ✅ |
| **Responsable :** Thuy-Trang Nguyen | |

---

#### 🟠 SPRINT 2 – Industrialisation & Déploiement (Heures 18 à 38) – Priorité HAUTE

**US-06 · EPIC-03 · 5 SP**
> *En tant que Dispatcheur RTE (Marc), je veux envoyer une requête JSON à un endpoint `POST /predict` et recevoir instantanément la prévision de charge en MW afin d'automatiser mes arbitrages de dispatching.*

| Critères d'acceptation | Statut |
|---|:---:|
| Validation des schémas d'entrée avec Pydantic (datetime ISO 8601 + temperature + lags optionnels) | ✅ |
| Valeurs par défaut intelligentes si lags absents (55 000 MW baseline) | ✅ |
| Réponse JSON : `prediction_mw`, `status`, `model_used`, `latency_sec`, `datetime` | ✅ |
| Latence d'inférence < 10 ms pour une requête unitaire | ✅ |
| **Responsable :** Djamel Chebbah | |

---

**US-07 · EPIC-03 · 3 SP**
> *En tant qu'Ingénieur MLOps (Dorian), je veux des endpoints `/health` et `/metrics` opérationnels afin que Kubernetes et Prometheus puissent surveiller et orchestrer l'API en production.*

| Critères d'acceptation | Statut |
|---|:---:|
| `GET /health` → `{"status": "ok"}` si modèle chargé, `{"status": "unhealthy"}` sinon | ✅ |
| `GET /metrics` → format Prometheus avec `http_requests_total`, `inference_latency_seconds`, `predicted_consumption_megawatts` | ✅ |
| Kubernetes `livenessProbe` et `readinessProbe` configurées sur `/health` | ✅ |
| **Responsable :** Djamel Chebbah | |

---

**US-08 · EPIC-03 · 5 SP**
> *En tant qu'Ingénieur MLOps, je veux un Dockerfile multi-stage sécurisé (non-root) afin que l'image de production soit minimale, sans outils de build, et exécutée sans privilèges root.*

| Critères d'acceptation | Statut |
|---|:---:|
| Build multi-stage : `builder` (compilation) + `runner` (production uniquement) | ✅ |
| Utilisateur non-root `appuser` (UID/GID 999) dans l'image finale | ✅ |
| Réduction de la taille d'image ≥ 50 % par rapport à une image mono-stage | ✅ |
| Scan Trivy : zéro CVE critique ou élevée | ✅ |
| **Responsable :** Djamel Chebbah | |

---

**US-09 · EPIC-03 · 5 SP**
> *En tant qu'Ingénieur MLOps, je veux des manifestes Kubernetes (Deployment, Service, HPA) afin d'assurer la haute disponibilité, l'autoscaling et les mises à jour sans interruption de service.*

| Critères d'acceptation | Statut |
|---|:---:|
| Deployment : 3 répliques, stratégie `RollingUpdate` (`maxUnavailable: 0`) | ✅ |
| Service : type `LoadBalancer`, port 80 → 8000 | ✅ |
| HPA : scale-out si CPU > 70 %, de 3 à 10 pods maximum | ✅ |
| `securityContext` : `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `capabilities: drop: [ALL]` | ✅ |
| **Responsable :** Djamel Chebbah | |

---

**US-10 · EPIC-03 · 5 SP**
> *En tant que Développeur MLOps, je veux un pipeline CI/CD GitHub Actions automatisé afin que chaque pull request déclenche les contrôles qualité, sécurité et tests avant tout merge.*

| Critères d'acceptation | Statut |
|---|:---:|
| Étape 1 : Linting – `black`, `flake8`, `mypy` (zéro erreur) | ✅ |
| Étape 2 : Tests – `pytest` avec couverture > 80 % (`pytest-cov`) | ✅ |
| Étape 3 : Sécurité – `bandit` (zéro faille moyenne/haute) + `trivy` (zéro CVE critique) | ✅ |
| Blocage automatique du merge si l'une des étapes échoue | ✅ |
| **Responsable :** Djamel Chebbah | |

---

**US-11 · EPIC-04 · 5 SP**
> *En tant qu'Ingénieur MLOps (Dorian), je veux un script de monitoring de drift hebdomadaire basé sur le test de Kolmogorov-Smirnov afin d'être alerté avant que la précision du modèle ne chute sous 5 %.*

| Critères d'acceptation | Statut |
|---|:---:|
| Test KS à deux échantillons sur la distribution de température (production vs entraînement) | ✅ |
| Seuil p-value < 0,05 → publication d'alerte ROUGE sur `/metrics` Prometheus | ✅ |
| Dashboard Grafana avec 3 niveaux : `✔ Nominal` · `⚠ Vigilance` · `✖ Critique` | ✅ |
| **Responsable :** Dorian Marty | |

---

**US-12 · EPIC-04 · 8 SP** *(ticketée sur 2 sous-tâches)*
> *En tant qu'Ingénieur MLOps, je veux un DAG Airflow hebdomadaire qui ré-entraîne un modèle Challenger et le promeut automatiquement si ses performances dépassent le Champion.*

| Critères d'acceptation | Statut |
|---|:---:|
| 4 tâches séquentielles : `extract_and_prepare_data` → `train_challenger` → `evaluate_and_compare` → promotion | ✅ |
| Promotion si et seulement si MAPE_challenger < MAPE_champion ET MAPE_challenger ≤ 5 % | ✅ |
| Alertes email sur `mlops-alerts@edf.fr` en cas d'échec (`email_on_failure: True`, `retries: 2`) | ✅ |
| **Responsable :** Dorian Marty | |

---

**US-13 · EPIC-04 · 3 SP**
> *En tant qu'Ingénieur de production, je veux un script de test de charge Locust simulant jusqu'à 1 000 utilisateurs concurrents afin de valider le SLA de latence (p95 < 200 ms) avant la mise en production.*

| Critères d'acceptation | Statut |
|---|:---:|
| Script Locust simulant des requêtes `POST /predict` avec températures et dates variables | ✅ |
| Scénario nominal : 100 users → p95 < 50 ms · taux erreur = 0 % | ✅ |
| Scénario de crête : 1 000 users → p95 < 200 ms · taux erreur = 0 % | ✅ |
| Rapport de résultats exporté | ✅ |
| **Responsable :** Dorian Marty | |

---

#### 🟡 BACKLOG DOCUMENTAIRE BLOC 4 – Priorité MOYENNE

**US-14 · EPIC-06 · 3 SP**
> *En tant que Sponsor EDF, je veux un dossier de cadrage complet avec WBS, roadmap et budget TCO afin de valider le périmètre et les ressources mobilisées.*
> **Responsable :** Noé Wibaut · **Statut :** ✅

**US-15 · EPIC-05 · 3 SP**
> *En tant que jury MSPR Bloc 4, je veux un cahier des charges fonctionnel et technique détaillé avec les user stories, personas et contraintes afin d'évaluer la maîtrise des spécifications.*
> **Responsable :** Thuy-Trang Nguyen · **Statut :** ✅

**US-16 · EPIC-06 · 5 SP**
> *En tant que Scrum Master (Djamel), je veux ce dossier de pilotage agile avec backlog, KPIs et tableaux de bord afin de formaliser la gouvernance agile du projet.*
> **Responsable :** Djamel Chebbah · **Statut :** 🔄 En cours

**US-17 · EPIC-07 · 3 SP**
> *En tant que Responsable Inclusion (Paul-Henri), je veux une charte de collaboration internationale et d'accessibilité WCAG 2.1 afin de garantir l'inclusion de tous les profils dans les 9 centres R&D EDF.*
> **Responsable :** Paul-Henri Dourneau · **Statut :** ✅

**US-18 · EPIC-08 · 3 SP**
> *En tant que Dispatcheur RTE (Marc), je veux comprendre les raisons des prédictions de l'IA via des fiches SHAP afin d'avoir confiance dans le système et de prendre des décisions éclairées.*
> **Responsable :** Noé Wibaut · **Statut :** ✅

---

### 1.3.3 Récapitulatif du Backlog par Sprint

| Sprint | US | SP Total | Responsable principal | Résultat |
|---|---|:---:|---|---|
| **Sprint 1** | US-01, US-02, US-03, US-04, US-05 | **24 SP** | Thuy-Trang · Paul-Henri | 24 SP livrés ✅ |
| **Sprint 2** | US-06, US-07, US-08, US-09, US-10, US-11, US-12, US-13 | **39 SP** | Djamel · Dorian · Noé | 39 SP livrés ✅ |
| **Documentation** | US-14, US-15, US-16, US-17, US-18 | **17 SP** | Noé · Paul-Henri · Djamel | En cours 🔄 |
| **TOTAL BACKLOG** | **18 US** | **80 SP** | | |

---

## 1.4 Déroulement des Itérations

### 1.4.1 Vue d'Ensemble des Sprints

```
SPRINT 1 – "Fondations Data & IA"           SPRINT 2 – "Industrialisation & Déploiement"
[H0 ──────────────── H18]                   [H18 ──────────────────────────── H38]
│                                            │
├── Sprint Planning (H0, 1h)                ├── Sprint Planning (H18, 1h)
├── Développement (H1 → H15)               ├── Développement (H19 → H35)
│   · Ingestion API ODRE                    │   · API FastAPI (/predict, /health, /metrics)
│   · Feature Engineering (13 features)     │   · Dockerfile multi-stage non-root
│   · Entraînement 4 modèles                │   · Manifestes Kubernetes (K8s/)
│   · Rapport de performance                │   · Pipeline CI/CD GitHub Actions
│                                            │   · Tests Locust (100 → 1 000 users)
├── Sprint Review (H15, 30min)             ├── Sprint Review (H35, 30min)
│   · Démo modèle KNN champion              │   · Démo API en production GCP
│   · Validation métriques jury             │   · Validation tests de charge
│                                            │
└── Rétrospective (H16, 30min)              └── Rétrospective (H36, 30min)
    · Bloqueur RBFN résolu                      · Optimisation CI/CD pipeline
    · Ajustement Sprint 2                        · Synthèse des enseignements
```

### 1.4.2 Les 5 Cérémonies Scrum en Détail

#### A. Sprint Planning

**Format :** Réunion synchrone de **1 heure** · Support : Jira + tableau Miro

| Phase | Durée | Contenu | Participants |
|---|:---:|---|---|
| **Partie 1 – Le QUOI** | 30 min | Le PO présente les US prioritaires du Product Backlog. L'équipe pose des questions de clarification. Les US retenues pour le sprint sont définies. | PO + Équipe + SM |
| **Partie 2 – Le COMMENT** | 30 min | L'équipe décompose chaque US en sous-tâches techniques (≤ 4h chacune). Estimation en SP via Planning Poker (cartes 1-2-3-5-8-13). Définition de l'objectif du sprint. | Équipe + SM |

**Règle de Planning Poker :**
- Si l'écart entre les estimations est ≥ 3 niveaux (ex: 1 vs 8), discussion obligatoire avant revote.
- Une US estimée à 13 SP est systématiquement décomposée en sous-tâches.
- La capacité du sprint est calculée : `Capacité = (Vélocité historique) × (Facteur de disponibilité)`

**Exemple de Sprint Planning Sprint 2 :**

| US | Estimation initiale | Discussion | Estimation finale |
|---|:---:|---|:---:|
| US-06 : API /predict | 5 vs 3 | Djamel explique la validation Pydantic complexe | **5 SP** |
| US-08 : Dockerfile multi-stage | 3 vs 5 | Paul-Henri soulève le défi du user non-root | **5 SP** |
| US-12 : DAG Airflow | 8 vs 13 | Dorian → décompose en 2 sous-tâches de 4h max | **8 SP** |

#### B. Daily Standup (Asynchrone – Format Écrit)

**Format :** Message écrit sur `#daily-standup` Slack/Teams · Avant 10h00 chaque jour de sprint

**Template standardisé :**
```
📅 Daily – [Prénom] – [Date]

✅ TERMINÉ HIER :
→ [Tâche complétée avec lien Jira]

🔄 EN COURS AUJOURD'HUI :
→ [Tâche planifiée avec lien Jira]

🚨 BLOQUEUR (si applicable) :
→ [Description du blocage + besoin d'aide]
   @[Personne concernée]
```

**Exemple de Daily réel (Sprint 2 – Jour 3) :**
```
📅 Daily – Djamel – Heure 23

✅ TERMINÉ HIER :
→ Dockerfile multi-stage validé (US-08) ✅
   → Image runner : 287 Mo (vs 640 Mo mono-stage) → -55 % ✅
   → Trivy scan : 0 CVE critique ✅

🔄 EN COURS AUJOURD'HUI :
→ Manifestes Kubernetes (US-09) – deployment.yaml + service.yaml
   → Lien Jira : EDF-034

🚨 BLOQUEUR :
→ Port 8000 bloqué par le firewall GCP du projet
   → @Dorian : Peut-tu ouvrir le port dans la console Cloud ?
```

**Règle de gestion des bloqueurs :**
- Bloqueur signalé → Scrum Master doit proposer une solution dans les **4 heures**.
- Si non résolu en **24 heures** → escalade au sponsor ou au référent technique concerné.

#### C. Sprint Review

**Format :** Réunion synchrone de **30 à 45 minutes** · Participants : Équipe + PO + Référents métier (Marc, Léa) + Sponsor (en option)

| Ordre du jour | Durée | Responsable |
|---|:---:|---|
| Introduction et rappel de l'objectif du sprint | 5 min | Scrum Master |
| **Démonstration des incréments livrés** (live, pas de slides) | 20 min | Membres de l'équipe |
| Questions et feedback des référents métier | 10 min | Marc / Léa |
| Mise à jour du Product Backlog en fonction des retours | 5 min | PO |

**Démonstrations effectuées :**

*Sprint Review 1 :*
- Exécution en live de `train_evaluate.py` → affichage du tableau comparatif des 4 modèles
- Démonstration de l'API ODRE et du fallback synthétique
- Présentation du graphique d'erreur MAPE par modèle → validation du KNN comme champion

*Sprint Review 2 :*
- Appel `POST /predict` en direct via Swagger UI sur l'instance GCP → prédiction en < 10 ms
- Démonstration du test de charge Locust en temps réel (100 → 1 000 users simulés)
- Affichage du dashboard Grafana avec les métriques Prometheus en live
- Test de rollback Kubernetes : `kubectl rollout undo` → retour en < 30 s démontré

#### D. Rétrospective

**Format :** Réunion synchrone de **30 minutes** · Outil : Miro (tableau virtuel) · Équipe uniquement (sans sponsor ni métier)

**Méthode utilisée : Starfish (5 axes)**

```
┌─────────────────────────────────────────────────────────────┐
│                RÉTROSPECTIVE – MÉTHODE STARFISH              │
│                                                             │
│  ⭐ START         │  📈 MORE          │  ✅ KEEP           │
│  Commencer à      │  Faire davantage   │  Continuer à faire │
│  faire            │                    │                    │
│                   │                    │                    │
│  ──────────────────────────────────────────────────────────  │
│  📉 LESS          │  🛑 STOP           │                    │
│  Faire moins de   │  Arrêter de faire  │                    │
│                   │                    │                    │
└─────────────────────────────────────────────────────────────┘
```

**Résultats de la Rétrospective Sprint 1 :**

| Axe | Éléments identifiés | Action décidée |
|---|---|---|
| **STOP** | Attendre la validation RBFN avant de passer à l'API (couplage trop fort) | Parallélisation des tâches US-05 et US-06 dans Sprint 2 |
| **MORE** | Écrire les tests Pytest pendant le développement (pas après) | TDD appliqué dès Sprint 2 |
| **KEEP** | Daily asynchrone sur Slack → efficace, pas de friction | Maintenu tel quel en Sprint 2 |
| **START** | Documenter le choix de chaque hyperparamètre dans le code | Ajout de commentaires systématiques |
| **LESS** | Réunions longues pour des décisions qui auraient pu être asynchrones | Max 2 réunions sync/sprint hors cérémonies obligatoires |

**Résultats de la Rétrospective Sprint 2 :**

| Axe | Éléments identifiés | Action pour la suite |
|---|---|---|
| **STOP** | Tester manuellement l'API avant de configurer le CI/CD (perte de temps) | Pipeline CI déclenché dès le premier commit sur une branche feature |
| **MORE** | Partage des logs de déploiement GCP dans le canal `#mlops-k8s` | Intégration webhook GCP → Slack |
| **KEEP** | Planning Poker pour les estimations → consensus rapide | Maintenu pour les US documentaires |
| **START** | Créer un template de rapport de drift automatique | Script de rapport hebdomadaire ajouté au DAG |

#### E. Backlog Refinement (Grooming)

**Format :** Réunion semi-synchrone de **45 minutes** · Fréquence : milieu de sprint

**Objectifs :**
1. Préparer les US du prochain sprint : clarifier les critères d'acceptation, lever les ambiguïtés.
2. Évaluer les nouvelles US issues des retours de la Sprint Review précédente.
3. Supprimer ou reporter les US dont la priorité a évolué.

**Règle :** Le PO ne doit pas presenter plus de US que l'équipe peut traiter en 2 sprints futurs.

---

### 1.4.3 Definition of Done (DoD) et Definition of Ready (DoR)

#### Definition of Done (DoD) – Critères de Complétude

Une User Story est considérée comme **« Terminée »** (*Done*) si et seulement si **tous** les critères suivants sont validés :

| # | Critère | Outil de vérification | Responsable de vérification |
|:---:|---|---|---|
| **1** | Code revu par au moins 1 autre membre de l'équipe via Pull Request | GitHub Pull Request Review | N'importe quel membre |
| **2** | Formatage automatique conforme (`black` sans avertissement) | CI/CD – Étape 1 | CI automatique |
| **3** | Vérification de style syntaxique (`flake8` : 0 avertissement) | CI/CD – Étape 1 | CI automatique |
| **4** | Typage statique validé (`mypy` : 0 avertissement sur modules modifiés) | CI/CD – Étape 1 | CI automatique |
| **5** | Tests unitaires passés avec couverture ≥ **80 %** (`pytest-cov`) | CI/CD – Étape 2 | CI automatique |
| **6** | Analyse de sécurité statique `Bandit` : 0 faille de criticité moyenne ou haute | CI/CD – Étape 3 | CI automatique |
| **7** | Scan de vulnérabilités `Trivy` : 0 CVE critique ou élevée | CI/CD – Étape 3 | CI automatique |
| **8** | Métriques d'entraînement et artefact modèle enregistrés dans MLflow (JSON) | Registre ML JSON | Data Scientist |
| **9** | Code déployé et fonctionnel sur l'environnement de staging | `kubectl get pods` – tous Running | Ingénieur MLOps |
| **10** | Documentation ou commentaire mis à jour si modification de l'API publique | Revue PR | Product Owner |

> ⚠️ **Règle absolue :** Si un seul critère de la DoD n'est pas validé à la fin du sprint, la US est rebasculée dans le Product Backlog. Elle n'est jamais partiellement comptabilisée dans la vélocité.

#### Definition of Ready (DoR) – Critères de Préparation

Une User Story peut entrer dans un Sprint Planning si elle respecte les critères de **« Prêt »** (*Ready*) :

| # | Critère | Exemple |
|:---:|---|---|
| **1** | Rédigée selon le format standard (*En tant que… je veux… afin de…*) | US-06 : *En tant que Dispatcheur RTE, je veux POST /predict...* |
| **2** | Critères d'acceptation rédigés, mesurables et testables | *Latence p95 < 200 ms mesurée par Locust* |
| **3** | Dépendances avec d'autres US clairement identifiées | *US-06 dépend de US-02 (pipeline features)* |
| **4** | Estimée en Story Points par l'équipe (Planning Poker) | *5 SP – consensus atteint* |
| **5** | Aucune ambiguïté technique non résolue | Pas de question ouverte dans les commentaires Jira |
| **6** | Priorisée et placée dans le Sprint Backlog par le PO | Position dans la colonne "To Do" sur Jira |

---

# 2. Tableaux de Bord de Suivi de Projet

> **Responsable de cette partie (Bloc 4) : Djamel Chebbah** – Agile management & tracking

---

## 2.1 Liste des KPI Projet

### 2.1.1 KPIs d'Avancement (Progression)

| KPI | Description | Formule / Méthode de calcul | Cible | Fréquence |
|---|---|---|:---:|:---:|
| **Vélocité Sprint** | Nombre de Story Points livrés et validés (DoD) par sprint | Somme des SP des US en statut "Done" en fin de sprint | ≥ 22 SP | Par sprint |
| **Burn-down Progress** | Écart entre la courbe idéale et la courbe réelle de consommation des SP | SP restants = Total Sprint - SP livrés cumulés | Écart < 20 % | Quotidien |
| **Taux de completion sprint** | % d'US livrées par rapport aux US engagées en Sprint Planning | (US Done / US Engagées) × 100 | ≥ 85 % | Par sprint |
| **Taux de spill-over** | % d'US reportées au sprint suivant non terminées | (US reportées / US Engagées) × 100 | ≤ 15 % | Par sprint |
| **Avancement WBS global** | % de livrables validés par rapport aux livrables planifiés | (Livrables Done / Livrables Planifiés) × 100 | 100 % à H+48 | Hebdo |

### 2.1.2 KPIs de Charges et Effort

| KPI | Description | Formule | Cible | Fréquence |
|---|---|---|:---:|:---:|
| **Charge consommée** | Heures réelles dépensées par membre et par tâche | Σ(temps_réel_tâche) par personne | ≤ 48 h au total | Quotidien |
| **Charge planifiée vs réelle** | Écart entre l'estimation Planning Poker et le temps réel passé | Δ = (Temps réel - Estimation) / Estimation × 100 % | Écart < 25 % | Par US |
| **Budget consommé** | Coût RH réel engagé vs budget initial de 3 000 € | Σ(heures × TJM/8) | ≤ 3 000 € | Hebdo |
| **Capacité disponible** | Heures productives disponibles par sprint par membre | Heures calendaires - Réunions - Absences | ≥ 8 h/pers/sprint | Par sprint |

### 2.1.3 KPIs de Qualité et Anomalies

| KPI | Description | Cible | Fréquence |
|---|---|:---:|:---:|
| **Taux de couverture de tests** | % de lignes de code couvertes par les tests Pytest | ≥ 80 % | Par commit |
| **Nombre de bugs critiques ouverts** | Tickets Jira de type "Bug" en statut "Open" avec sévérité Critique ou Haute | 0 | Quotidien |
| **Nombre de failles sécurité** | CVE critiques/élevées détectées par Trivy ou Bandit | 0 | Par PR |
| **Taux de réussite CI** | % de pipelines CI/CD passant sans erreur | ≥ 90 % | Quotidien |
| **MAPE modèle champion** | Précision du modèle KNN sur le jeu de test | < 5 % | Par entraînement |
| **Taux de drift KS détecté** | Proportion de semaines avec drift statistique (KS p < 0,05) | < 10 % / an | Hebdomadaire |

### 2.1.4 KPIs de Performance Opérationnelle

| KPI | Description | Cible | Fréquence |
|---|---|:---:|:---:|
| **Latence API p50** | Médiane du temps de réponse `/predict` | < 15 ms | Temps réel |
| **Latence API p95** | 95ème percentile du temps de réponse `/predict` | < 200 ms | Temps réel |
| **Débit (Throughput)** | Nombre de requêtes traitées par seconde | ≥ 45 req/s (100 users) | Temps réel |
| **Taux d'erreur HTTP 5xx** | % de réponses HTTP en erreur serveur | 0,0 % | Temps réel |
| **Uptime API** | Disponibilité de l'endpoint `/health` sur la période | ≥ 99,5 % | Mensuel |
| **MTTR (Mean Time To Repair)** | Temps moyen de résolution d'un incident | < 30 min (rollback) | Par incident |

### 2.1.5 KPIs de Vélocité et Agilité

| KPI | Valeur Sprint 1 | Valeur Sprint 2 | Tendance |
|---|:---:|:---:|:---:|
| **Vélocité réelle** | 24 SP | 39 SP | 📈 +63 % |
| **Taux de completion** | 100 % | 100 % | ✅ Stable |
| **Bloqueurs signalés** | 1 | 2 | ⚠️ Hausse |
| **Bloqueurs résolus** | 1 | 2 | ✅ Tous résolus |
| **Rétrospective actions mise en œuvre** | 3/5 | 4/5 | 📈 +1 |

---

## 2.2 Maquette de Tableau de Bord

### 2.2.1 Vue Sponsor (Direction Innovation EDF)

La vue Sponsor est conçue pour une lecture en **moins de 2 minutes**. Elle présente uniquement les informations stratégiques et les signaux d'alerte nécessaires à la prise de décision executive.

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║         TABLEAU DE BORD SPONSOR – PROJET EDF/RTE PREDICTOR           Juin 2026  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  🎯 OBJECTIFS MÉTIER                         📊 AVANCEMENT GLOBAL                ║
║  ┌─────────────────────────────────────┐     ┌───────────────────────────────┐   ║
║  │ MAPE modèle champion   4,68 % ✔    │     │ Story Points livrés : 63/80   │   ║
║  │ Seuil critique métier  < 5,0 %     │     │ [██████████████████░░░] 79 %  │   ║
║  │ Latence API p95        185 ms  ✔   │     │                               │   ║
║  │ SLA cible              < 200 ms    │     │ Sprint 1 ✅  Sprint 2 ✅       │   ║
║  │ Uptime API             99,8 %  ✔   │     │ Documentation 🔄              │   ║
║  └─────────────────────────────────────┘     └───────────────────────────────┘   ║
║                                                                                  ║
║  🚦 STATUT DES JALONS                         💰 BUDGET CONSOMMÉ                 ║
║  ┌─────────────────────────────────────┐     ┌───────────────────────────────┐   ║
║  │ J0 – Kick-off          ✅ H+0       │     │ Budget initial   : 3 000 €    │   ║
║  │ J1 – Backlog validé    ✅ H+6       │     │ Consommé         : 2 850 €    │   ║
║  │ J2 – Modèle champion   ✅ H+18      │     │ Reste            :   150 €    │   ║
║  │ J3 – API en production ✅ H+30      │     │ [█████████████████████░] 95 % │   ║
║  │ J4 – Livrables finaux  🔄 H+42      │     │                               │   ║
║  │ J5 – Soutenances jury  📅 H+48      │     │ ⚠️ Provision risque : 300 €   │   ║
║  └─────────────────────────────────────┘     └───────────────────────────────┘   ║
║                                                                                  ║
║  🔴 RISQUES ACTIFS               🟡 VIGILANCE             🟢 RÉSOLUS             ║
║  ┌──────────────────────────────────────────────────────────────────────────┐    ║
║  │ Aucun risque rouge actif │ Finalisation docs J4 (H+42) │ RBFN écarté ✅ │    ║
║  └──────────────────────────────────────────────────────────────────────────┘    ║
║                                                                                  ║
║  📅 PROCHAIN JALON : J4 – Livrables finaux (H+42) · Responsable : Noé Wibaut    ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

**Règles d'affichage de la vue Sponsor :**
- Pas de détail technique – uniquement des indicateurs de résultat.
- Signaux d'alerte visuels : ✅ = objectif atteint · ⚠️ = vigilance · 🔴 = action requise.
- Rafraîchissement : **hebdomadaire**, envoyé par le Scrum Master via email récapitulatif.

---

### 2.2.2 Vue Chef de Projet / Scrum Master

La vue Chef de Projet est conçue pour la **gestion opérationnelle quotidienne**. Elle contient le détail des sprints, des KPIs techniques et des bloqueurs.

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║    TABLEAU DE BORD CHEF DE PROJET / SCRUM MASTER               Sprint 2 – H+28  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  📈 BURN-DOWN CHART – SPRINT 2                                                   ║
║  ┌────────────────────────────────────────────────────────────────┐             ║
║  │ SP │                                                           │             ║
║  │ 40 │ \  (Courbe idéale)                                        │             ║
║  │ 35 │  \──────────────────────────────── Idéale                 │             ║
║  │ 30 │   * (Réelle – Jour 1 : 35 SP restants)                    │             ║
║  │ 25 │    *                                                       │             ║
║  │ 20 │     *──* (J3 : Déploiement GCP terminé – 20 SP restants)  │             ║
║  │ 15 │          *                                                 │             ║
║  │ 10 │           *──* (J5 : CI/CD OK – 10 SP restants)           │             ║
║  │  5 │                *                                          │             ║
║  │  0 │                 *── Fin Sprint (J7 : 0 SP) ✅             │             ║
║  │    └────────────────────────────────────────────────────────── │             ║
║  │       J1   J2   J3   J4   J5   J6   J7                        │             ║
║  └────────────────────────────────────────────────────────────────┘             ║
║                                                                                  ║
║  🎯 SPRINT BACKLOG – STATUT                                                      ║
║  ┌──────────────────┬──────┬─────────────┬──────────────────────┬────────────┐  ║
║  │ US               │  SP  │  Assigné à  │ Statut               │ DoD (%)    │  ║
║  ├──────────────────┼──────┼─────────────┼──────────────────────┼────────────┤  ║
║  │ US-06 /predict   │  5   │ Djamel      │ ✅ DONE              │ 100 %      │  ║
║  │ US-07 /health    │  3   │ Djamel      │ ✅ DONE              │ 100 %      │  ║
║  │ US-08 Dockerfile │  5   │ Djamel      │ ✅ DONE              │ 100 %      │  ║
║  │ US-09 K8s        │  5   │ Djamel      │ ✅ DONE              │ 100 %      │  ║
║  │ US-10 CI/CD      │  5   │ Djamel      │ ✅ DONE              │ 100 %      │  ║
║  │ US-11 Drift KS   │  5   │ Dorian      │ ✅ DONE              │ 100 %      │  ║
║  │ US-12 Airflow    │  8   │ Dorian      │ ✅ DONE              │ 100 %      │  ║
║  │ US-13 Locust     │  3   │ Dorian      │ ✅ DONE              │ 100 %      │  ║
║  └──────────────────┴──────┴─────────────┴──────────────────────┴────────────┘  ║
║                                                                                  ║
║  ⚡ PERFORMANCE API (Prometheus/Grafana – Live)                                  ║
║  ┌───────────────────────────────────────────────────────────────────────────┐   ║
║  │  Latence p50 : 12 ms ✅    │  Débit : 45 req/s ✅   │  Erreurs : 0,0% ✅ │   ║
║  │  Latence p95 : 35 ms ✅    │  Pods actifs : 3/3 ✅  │  MAPE : 4,68% ✅   │   ║
║  │  Dernière prédiction : 59 842 MW (03/06/2026 14:30)                       │   ║
║  └───────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                  ║
║  🚨 BLOQUEURS EN COURS                                                           ║
║  ┌───────────────────────────────────────────────────────────────────────────┐   ║
║  │ ID      │ Description                      │ Assigné │ Statut │ Échéance  │   ║
║  │ BLK-002 │ Port 8000 GCP firewall bloqué    │ Dorian  │ ✅ RÉSOLU H+23   │   ║
║  │ BLK-003 │ Drift KS : API ODRE down depuis  │ Paul-H  │ ⚠️ EN COURS H+30 │   ║
║  │         │ 2h → fallback activé              │         │        │          │   ║
║  └───────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                  ║
║  📊 QUALITÉ CI/CD (Derniers 10 pipelines)                                        ║
║  ┌───────────────────────────────────────────────────────────────────────────┐   ║
║  │  ✅✅✅✅✅✅✅✅✅✅  Taux réussite : 100 %                              │   ║
║  │  Couverture Pytest : 84 % ✅   │   Bandit : 0 faille ✅   │ Trivy : 0 ✅ │   ║
║  └───────────────────────────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 2.3 Utilisation des Indicateurs pour Anticiper et Corriger les Écarts

### 2.3.1 Processus de Revue des KPIs

Le Scrum Master (Djamel Chebbah) effectue une revue quotidienne des KPIs selon le processus suivant :

```
CYCLE DE SURVEILLANCE DES KPIs

[Quotidien]          [Bi-hebdomadaire]        [Par sprint]         [Annuel]
     │                      │                      │                   │
Vérifier le          Revue Burn-down         Sprint Review        Revue TCO
Burn-down            + bloqueurs             + Vélocité           + Budget
Drift KS             + Qualité CI            + DoD validées       + OPEX Cloud
Latence API          + Budget RH             + Rétrospective
     │                      │                      │
     ▼                      ▼                      ▼
Publication sur      Email résumé au         Rapport de sprint
canal #kpi-board     PO + Référents          envoyé au Sponsor
```

### 2.3.2 Exemples de Décisions Prises sur la Base des KPIs

#### Exemple 1 – Détection d'un risque de dérive du Burn-down (Sprint 1, Jour 4)

**Signal détecté :**
- Burn-down réel : 18 SP restants
- Burn-down idéal : 12 SP restants
- **Écart : +6 SP** → La courbe réelle est au-dessus de la courbe idéale → risque de spill-over

**Diagnostic (15 min de réunion d'urgence) :**
> L'implémentation du réseau RBFN (US-05, 8 SP) a pris 2 SP supplémentaires en raison de la complexité de l'interface compatible scikit-learn non anticipée lors du Planning Poker.

**Décision corrective prise :**
1. Dorian réalloue 2h de ses tâches de monitoring (non critiques pour Sprint 1) pour aider Thuy-Trang sur la compatibilité scikit-learn du RBFN.
2. Une sous-tâche de la US-05 (le test de performance du RBFN) est reportée en dehors du sprint critique (sera fait en parallèle du Sprint 2).
3. Le PO (Noé) valide que la US-05 est complète dès que l'interface est opérationnelle (les métriques RBFN suivront).

**Résultat :** Sprint 1 livré à 100 % · Spill-over = 0 %

---

#### Exemple 2 – Alerte de drift qualité CI (Sprint 2, Jour 2)

**Signal détecté :**
- Taux de réussite CI/CD : **70 %** (7/10 derniers pipelines)
- 3 échecs consécutifs sur la vérification `mypy` pour `app.py`

**Diagnostic :**
> Le type de retour de la fonction `load_model_and_pipeline()` n'était pas annoté, entraînant des erreurs mypy bloquant le merge de 2 Pull Requests.

**Décision corrective prise :**
1. Djamel ajoute une règle dans le template de PR : *"Vérifier mypy en local avant de soumettre la PR"*.
2. Ajout d'un script de pre-commit `mypy` obligatoire dans le `.pre-commit-config.yaml`.
3. La règle est formalisée dans la DoD (critère #3).

**Résultat :** Taux de réussite CI remonte à 100 % dans les 4 heures.

---

#### Exemple 3 – Décision de ne pas promouvoir le RBFN en production (Post Sprint 1)

**Signal détecté sur le KPI "MAPE modèle champion" :**

| Modèle | MAPE | Décision |
|---|:---:|:---:|
| KNN | **4,68 %** | ✅ Sélectionné champion |
| Random Forest | 4,87 % | ❌ Écarté (meilleur backup) |
| Decision Tree | 5,48 % | ❌ Écarté (dépasse seuil critique) |
| **RBFN** | **9,19 %** | 🛑 **Écarté immédiatement** |

**Décision prise par le PO (Noé Wibaut) après Sprint Review :**
> Le RBFN affiche un R² négatif (-0,36) et un MAPE de 9,19 %, soit presque le double du seuil critique de 5 %. Bien que l'effort de développement (4h) soit significatif, la règle RG-01 est non-négociable : le modèle mis en production doit avoir un MAPE < 5 %. Le KNN est sélectionné.

**Conséquence sur le backlog :**
- La US de déploiement du RBFN est retirée du backlog (Won't Do).
- Une US documentaire est ajoutée pour expliquer et archiver l'analyse comparative dans le rapport final.

---

#### Exemple 4 – Décision de scale-out K8s basée sur les métriques Locust

**Signal détecté sur le KPI "Latence API p95" pendant le test de crête :**
- Locust – 600 users : p95 = **195 ms** → Limite SLA atteinte !
- CPU average des 3 pods : **74 %** → Dépasse le seuil HPA de 70 %

**Décision automatique (déclenchée par le HPA Kubernetes) :**
> Le HPA détecte que l'utilisation CPU dépasse 70 % sur les 3 pods existants et instancie automatiquement 2 pods supplémentaires (total : 5 pods).

**Résultat mesuré 90 secondes après :**
- Locust – 600 users : p95 = **120 ms** → SLA respecté ✅
- Locust – 1 000 users (test de crête maximum) : p95 = **185 ms** ✅

**Décision humaine complémentaire (Djamel Chebbah) :**
> Le test confirme que le HPA est correctement configuré. Aucun ajustement nécessaire. La documentation du test de charge est complétée et le rapport Locust est versé dans le dépôt.

---

#### Exemple 5 – Réallocation budgétaire suite à dépassement de charge

**Signal détecté sur le KPI "Charge consommée" (Jour 30) :**
- Paul-Henri Dourneau : 16h consommées (estimation initiale : 10h)
- Cause : L'API ODRE a changé son format JSON en cours de projet, nécessitant une refactorisation du parser

**Décision corrective :**
1. La provision pour risques de 300 € (10 % du budget projet) est activée pour absorber les heures supplémentaires.
2. Pour les sprints futurs, un délai de 2h est systématiquement ajouté aux US d'intégration d'API tierce pour couvrir les changements de format.
3. Paul-Henri délègue la rédaction des slides Bloc 4 à Noé pour libérer du temps de développement.

**Résultat :** Budget total maîtrisé en dessous de 3 300 € · Livraison dans les délais.

---

# 3. Pilotage des Prestataires & du SI Existant

> **Responsable de cette partie (Bloc 4) : Djamel Chebbah** – Agile management & tracking

---

## 3.1 Cartographie des Prestataires et Systèmes Connectés

### 3.1.1 Vue d'Ensemble de l'Écosystème

```
                    ┌──────────────────────────────────────────────────────┐
                    │             PROJET EDF/RTE PREDICTOR                 │
                    │          (API FastAPI sur Kubernetes GCP)            │
                    └────────────────────────┬─────────────────────────────┘
                                             │
              ┌──────────────────────────────┼──────────────────────────────┐
              │                             │                              │
              ▼                             ▼                              ▼
  ┌─────────────────────┐      ┌────────────────────────┐    ┌────────────────────────┐
  │  FOURNISSEURS       │      │  SYSTÈMES SI INTERNES  │    │  HÉBERGEURS CLOUD      │
  │  DE DONNÉES         │      │  EDF / RTE             │    │  & OUTILS MLOps        │
  ├─────────────────────┤      ├────────────────────────┤    ├────────────────────────┤
  │ • ODRE / RTE        │      │ • Console supervision  │    │ • Google Cloud Platform │
  │   (Eco2mix API)     │      │   RTE (Dispatcher UI)  │    │   (VM + K8s Cluster)   │
  │   [Données Conso]   │      │ • SI EDF Trading       │    │ • Azure (ACR Registry) │
  │                     │      │   (EPEX SPOT)          │    │ • GitHub (CI/CD SCM)   │
  │ • Météo-France      │      │ • Systèmes historiques │    │ • Prometheus (SaaS)    │
  │   (Synop Synoptique │      │   Excel existants      │    │ • Grafana Cloud        │
  │   Températures)     │      │   (processus As-Is)    │    │ • MLflow (local JSON)  │
  │                     │      │                        │    │ • Docker Hub / ACR     │
  │ • Bibliothèque      │      │ • Portail Git EDF      │    │ • Apache Airflow       │
  │   `holidays` (PyPI) │      │   (Confluence/Jira)    │    │   (DAG hebdomadaire)   │
  └─────────────────────┘      └────────────────────────┘    └────────────────────────┘
              │                             │                              │
              └──────────────────────────────┼──────────────────────────────┘
                                             │
                              ┌──────────────▼──────────────┐
                              │   UTILISATEURS FINAUX       │
                              │ • Dispatcheurs RTE (Marc)   │
                              │ • Analystes EDF (Léa)       │
                              │ • Ingénieurs MLOps          │
                              └─────────────────────────────┘
```

### 3.1.2 Fiches Systèmes & Prestataires

#### Système 1 – ODRE / API Eco2mix RTE

| Attribut | Détail |
|---|---|
| **Nature** | Fournisseur de données publiques (Open Data) |
| **Gestionnaire** | RTE – Réseau de Transport d'Électricité |
| **Rôle dans le projet** | Source de données principale de consommation électrique nationale demi-horaire |
| **URL / Endpoint** | `https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-national-tr/records` |
| **Format de données** | JSON – Champs : `date_heure`, `consommation` (MW), `temperature` (optionnel) |
| **Fréquence de rafraîchissement** | 30 minutes (données quasi-temps réel) |
| **Disponibilité connue** | Variable – Pannes possibles lors des maintenances RTE |
| **Stratégie de résilience** | Fallback automatique vers données synthétiques si timeout > 5 s |
| **Criticité pour le projet** | **Haute** (source principale) |
| **Contact technique** | opensource@rte-france.com |

---

#### Système 2 – Météo-France (Données Synoptiques)

| Attribut | Détail |
|---|---|
| **Nature** | Fournisseur de données météorologiques (partiellement public) |
| **Rôle dans le projet** | Données de température nationale pour le feature engineering |
| **Intégration actuelle** | **Simulée** dans le pipeline via modèle mathématique haute fidélité (cycles saisonniers + journaliers) |
| **Intégration cible (To-Be)** | Intégration directe de l'API Météo-France Data (avec abonnement professionnel EDF) |
| **Format de données** | JSON / CSV – Température nationale moyenne par créneau demi-horaire |
| **Criticité pour le projet** | **Haute** (composante majeure de la thermosensibilité) |
| **Limite actuelle** | Données météo simulées dans la version académique ; à remplacer par données réelles en production |

---

#### Système 3 – Google Cloud Platform (Infrastructure de déploiement)

| Attribut | Détail |
|---|---|
| **Nature** | Hébergeur Cloud – Fournisseur d'Infrastructure (IaaS) |
| **Gestionnaire EDF** | Djamel Chebbah (VM GCP personnelle pour le projet académique) |
| **Rôle dans le projet** | Hébergement du cluster Kubernetes + déploiement de l'API FastAPI |
| **Services utilisés** | Google Compute Engine (VM) · Google Kubernetes Engine (GKE) |
| **SLA Cloud** | Uptime garanti ≥ 99,9 % (SLA GCP) |
| **Sécurité** | Firewall VPC · HTTPS · IAM avec principe du moindre privilège |
| **Coût** | Projet académique : VM partagée (coût marginal) |
| **Alternatives en production EDF** | Azure AKS (préféré EDF) · AWS EKS |

---

#### Système 4 – Azure Container Registry (Registre Docker)

| Attribut | Détail |
|---|---|
| **Nature** | Registre d'images Docker managé (PaaS) |
| **Rôle dans le projet** | Stockage versionné des images Docker de l'API (`predictor-api:<sha-commit>`) |
| **Intégration** | Push automatique par le pipeline CI/CD GitHub Actions après chaque build réussi |
| **Tarification** | Offre Standard – 0,56 €/jour = **204,40 €/an** |
| **SLA** | Uptime ≥ 99,9 % (SLA Azure) |
| **Politique de rétention** | Conservation des 5 dernières images taguées + tags Git |

---

#### Système 5 – GitHub & GitHub Actions (SCM & CI/CD)

| Attribut | Détail |
|---|---|
| **Nature** | Plateforme de contrôle de version et d'intégration continue |
| **Rôle dans le projet** | Versioning du code · Automatisation CI/CD · Revue de code (Pull Requests) |
| **Déclencheurs CI** | Push sur `feature/*` ou `fix/*` · Pull Request vers `main` |
| **Étapes CI** | Lint → Tests → Scans Sécurité → Build Docker → Push ACR → Deploy K8s |
| **Accès** | Dépôt `noewib/MSPR3` · Équipe de 5 contributeurs |
| **Coût** | Plan gratuit (Actions 2 000 min/mois) |

---

#### Système 6 – Apache Airflow (Orchestration MLOps)

| Attribut | Détail |
|---|---|
| **Nature** | Orchestrateur de workflows (DAG) pour le MLOps |
| **Rôle dans le projet** | Automatisation du ré-entraînement hebdomadaire (Champion vs Challenger) |
| **DAG** | `edf_consumption_predictor_retraining` · Planification : `@weekly` (Lundi 00h00) |
| **Mode d'intégration** | Simulé localement (MockDAG) pour l'environnement académique ; Airflow complet en production |
| **Alertes** | Email automatique sur `mlops-alerts@edf.fr` en cas d'échec de tâche |

---

#### Système 7 – Consoles Supervision RTE (SI Existant Cible)

| Attribut | Détail |
|---|---|
| **Nature** | Système d'information opérationnel de RTE (existant, non modifié) |
| **Rôle dans le projet** | **Système consommateur** de l'API : affiche les prédictions dans l'interface des dispatcheurs |
| **Intégration prévue** | L'API `/predict` est appelée par la console RTE toutes les 30 min · Réponse JSON intégrée dans les écrans de supervision |
| **Contrainte d'intégration** | SLA de latence < 200 ms obligatoire · Format JSON standardisé · HTTPS uniquement |
| **Processus As-Is** | Excel manuel + extrapolation empirique |
| **Processus To-Be** | Appel API automatique → Alerte proactive → Validation humaine (Human-in-the-loop) |

---

## 3.2 Rôles & Responsabilités (RACI Prestataires)

### 3.2.1 Matrice RACI des Systèmes & Prestataires

| Activité / Système | Équipe Projet | SM (Djamel) | PO (Noé) | RTE / ODRE | Météo-France | GCP/Azure | DSI EDF |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Intégration API ODRE** | R | C | I | A | — | — | I |
| **Gestion du fallback données** | R | C | I | I | — | — | — |
| **Déploiement cluster K8s (GCP)** | R | A | I | — | — | C | I |
| **Gestion du registre Docker (ACR)** | R | A | I | — | — | C | — |
| **Pipeline CI/CD (GitHub Actions)** | R | A | I | — | — | — | I |
| **Monitoring Prometheus/Grafana** | R | A | I | — | — | C | I |
| **DAG Airflow (ré-entraînement)** | R | A | I | — | — | — | I |
| **Intégration console supervision RTE** | C | I | A | R | — | — | C |
| **Conformité RGPD** | R | C | A | C | — | — | A |
| **SLA Cloud (uptime 99,5 %)** | — | A | I | — | — | R | C |
| **Accès données Météo-France** | C | I | A | — | R | — | C |

*R : Réalise · A : Approuve · C : Consulté · I : Informé*

### 3.2.2 Responsabilités par Interlocuteur

| Interlocuteur | Référent Équipe | Niveau de criticité | Nature de la relation |
|---|---|:---:|---|
| **ODRE / RTE (API Eco2mix)** | Paul-Henri Dourneau | 🔴 Haute | Dépendance fonctionnelle (source de données principale) |
| **Météo-France** | Paul-Henri Dourneau | 🟠 Moyenne | Dépendance simulée en académique, réelle en production |
| **Google Cloud Platform** | Djamel Chebbah | 🔴 Haute | Infrastructure d'hébergement et de déploiement |
| **Azure (ACR)** | Djamel Chebbah | 🟠 Moyenne | Registre Docker – disponibilité importante pour CI/CD |
| **GitHub / GitHub Actions** | Djamel Chebbah | 🟠 Moyenne | SCM et automatisation CI/CD |
| **Apache Airflow** | Dorian Marty | 🟡 Faible (académique) | Orchestration MLOps – simulé localement |
| **DSI EDF / RTE** | Noé Wibaut (PO) | 🔴 Haute | Validation architecture, conformité sécurité, RGPD |
| **Dispatcheurs RTE** | Thuy-Trang Nguyen | 🔴 Haute | Utilisateurs finaux – validation fonctionnelle |

---

## 3.3 Modalités de Pilotage des Prestataires

### 3.3.1 Comités et Rituels de Pilotage

| Comité | Fréquence | Participants | Objet | Animateur |
|---|:---:|---|---|---|
| **Comité Projet** (COPRO) | Hebdomadaire (Lundi 14h00-15h00 CET) | Équipe + PO + SM + Référents métier | Avancement global · KPIs · Bloqueurs · Décisions | Djamel Chebbah (SM) |
| **Comité Technique** (COTECH) | Bi-hebdomadaire (Mercredi 14h00-14h30 CET) | Équipe dev/data + SM | Revue technique · Code review · Architecture · Sécurité | Dorian Marty |
| **Comité Stratégique** (COSTRAT) | Par jalon (J1, J2, J3, J4) | PO + Sponsor + Référents métier | Validation jalons · Budget · Risques stratégiques · Go/No-Go | Noé Wibaut (PO) |
| **Point Cloud** | Mensuel | Djamel + Équipe GCP | Consommation ressources · Coûts · Incidents Cloud | Djamel Chebbah |
| **Revue Sécurité** | Par sprint | Djamel + DSI EDF | Rapport Bandit/Trivy · Vulnérabilités · RGPD | Djamel Chebbah |

#### Règle de la Fenêtre de Communication Universelle

Tous les comités sont planifiés exclusivement sur la plage **14h00 – 16h00 (heure de Paris / CET)**, correspondant à la fenêtre de recouvrement maximale des 9 centres R&D mondiaux d'EDF :

| Ville | Heure locale |
|---|---|
| Paris (France) | **14h00 – 16h00** |
| Londres (Royaume-Uni) | 13h00 – 15h00 |
| Munich / Rome (Europe) | 14h00 – 16h00 |
| New York (États-Unis) | 08h00 – 10h00 |
| Pékin (Chine) | 20h00 – 22h00 *(limité aux points essentiels)* |

### 3.3.2 SLA (Service Level Agreements) par Système

#### SLA des Systèmes Externes Critiques

| Système | SLA Uptime | Délai de réponse max | Action si SLA non respecté |
|---|:---:|:---:|---|
| **API ODRE (Eco2mix)** | Non garanti (open data) | 5 s (timeout) | Déclenchement automatique du fallback synthétique |
| **Google Cloud Platform** | 99,9 % (SLA GCP) | N/A (infrastructure) | Incident reporté + escalade à l'équipe Support GCP |
| **Azure ACR** | 99,9 % (SLA Azure) | N/A (registre) | Bascule sur Docker Hub en secours |
| **GitHub Actions** | 99,9 % (SLA GitHub) | N/A (CI/CD) | Déclenchement manuel de l'étape CI via script local |

#### SLA Internes de l'API Predictor EDF

| Indicateur SLA | Valeur cible | Mesure | Pénalité si non respecté |
|---|:---:|---|---|
| **Uptime API** | ≥ 99,5 % | Prometheus `http_requests_total` errors | Escalade immédiate + rapport d'incident |
| **Latence p95 (nominale)** | < 200 ms | Histogram `inference_latency_seconds` | Analyse + optimisation du modèle ou de l'infrastructure |
| **Taux d'erreur HTTP 5xx** | 0,0 % | Counter `http_requests_total` status=5xx | Rollback immédiat si persistant > 5 min |
| **MAPE modèle** | < 5 % | Evaluation hebdomadaire | Déclenchement du DAG de ré-entraînement |
| **Rollback time** | < 30 s | `kubectl rollout undo` + readiness | Post-mortem si dépassé |

### 3.3.3 Livrables et Points de Contrôle par Prestataire

#### Système ODRE / RTE – Points de contrôle

| Livrable / Point de contrôle | Fréquence | Responsable | Critère de validation |
|---|:---:|---|---|
| Validation du format JSON de l'API | À chaque changement de version API | Paul-Henri Dourneau | Script de validation automatique (tests d'intégration) |
| Test de disponibilité du fallback | Mensuel | Paul-Henri Dourneau | Simulation de panne → données synthétiques générées OK |
| Rapport de disponibilité API ODRE | Mensuel | Paul-Henri Dourneau | Taux de succès des appels > 90 % |

#### Infrastructure Cloud (GCP / Azure) – Points de contrôle

| Livrable / Point de contrôle | Fréquence | Responsable | Critère de validation |
|---|:---:|---|---|
| Rapport de consommation Cloud | Mensuel | Djamel Chebbah | Coût ≤ budget prévu (< 145 €/mois) |
| Audit de configuration K8s | Par déploiement | Djamel Chebbah | `kubectl get pods` → 3/3 Running · HPA opérationnel |
| Test de restauration (DR) | Trimestriel | Djamel Chebbah | Rollback Kubernetes < 30 s · Aucune perte de données |
| Rapport sécurité (Trivy + Bandit) | Par sprint | Djamel Chebbah | 0 CVE critique · 0 faille Bandit moyenne/haute |

#### GitHub Actions – Points de contrôle CI/CD

| Livrable / Point de contrôle | Fréquence | Responsable | Critère de validation |
|---|:---:|---|---|
| Tableau de bord CI (taux de réussite) | Quotidien | Djamel Chebbah | Taux de réussite ≥ 90 % |
| Rapport de couverture Pytest | Par PR | Djamel Chebbah | Couverture ≥ 80 % sur les modules modifiés |
| Alerte sur pipeline en échec | Immédiat (webhook Slack) | CI/CD automatique | Notification dans `#mlops-k8s` dans les 5 min |

#### DSI EDF / Référent Sécurité – Points de contrôle

| Livrable / Point de contrôle | Fréquence | Responsable | Critère de validation |
|---|:---:|---|---|
| Rapport de sécurité applicative | Par sprint | Djamel Chebbah → DSI EDF | Bandit 0 faille haute · Trivy 0 CVE critique |
| Revue de conformité RGPD | Trimestriel | Noé Wibaut (PO) | Aucune donnée personnelle · Registre des traitements à jour |
| Audit d'architecture | Par jalon majeur | Dorian Marty → DSI EDF | Validation du schéma d'architecture · SecContext K8s |

### 3.3.4 Procédure de Gestion des Incidents Prestataires

#### Matrice d'Escalade

```
INCIDENT DÉTECTÉ
      │
      ▼
Sévérité P1 (Critique) ?  ──► Oui ──► Escalade IMMÉDIATE
[API down > 5 min]                     → Scrum Master (Djamel)
[MAPE > 8 %]                           → PO (Noé)
[Faille sécurité critique]             → DSI EDF
                                       → Rollback si nécessaire
      │ Non
      ▼
Sévérité P2 (Haute) ?  ──► Oui ──► Escalade dans 2h
[Drift KS rouge]                       → Membre responsable
[Latence p95 > 200 ms]                 → Scrum Master informé
[Pipeline CI > 3 échecs]               → Comité Technique suivant
      │ Non
      ▼
Sévérité P3 (Normale) ?  ──► Résolution dans 24h
[API ODRE indisponible]                → Fallback activé
[Warning Bandit mineur]                → Ticket Jira créé
[Couverture test 78 %]                 → PR bloquée · Correction requise
```

#### Processus de Résolution (5 étapes)

| Étape | Action | Responsable | Délai max |
|:---:|---|---|:---:|
| **1. Détection** | Alerte Prometheus/Grafana ou signalement équipe | Automatique / Tout membre | Immédiat |
| **2. Qualification** | Détermination de la sévérité (P1/P2/P3) | Scrum Master | 15 min |
| **3. Mitigation** | Application de la solution de contournement (fallback, rollback…) | Responsable technique | P1 : 30 min · P2 : 2h · P3 : 24h |
| **4. Résolution** | Correction définitive et validation | Responsable technique + Code review | Variable selon complexité |
| **5. Post-mortem** | Analyse des causes racines + actions préventives | Scrum Master + Équipe | 48h après résolution |

---

## Conclusion du Dossier de Pilotage Agile

Ce dossier formalise l'ensemble du dispositif de gouvernance agile mis en œuvre pour piloter le projet EDF/RTE de prédiction de consommation électrique. Il démontre la maîtrise des pratiques Scrum adaptées à un contexte MLOps industriel interculturel.

### Synthèse des Résultats Agiles

| Indicateur | Valeur finale | Cible | Statut |
|---|:---:|:---:|:---:|
| **Vélocité totale** | 63 SP livrés | 50 SP | ✅ +26 % |
| **Taux de completion sprints** | 100 % | ≥ 85 % | ✅ |
| **Bloqueurs résolus** | 3/3 | 100 % | ✅ |
| **Actions rétro implémentées** | 7/10 | ≥ 60 % | ✅ |
| **MAPE champion (KNN)** | 4,68 % | < 5 % | ✅ |
| **Taux CI réussite** | 100 % | ≥ 90 % | ✅ |
| **Couverture Pytest** | 84 % | ≥ 80 % | ✅ |
| **Budget consommé** | 2 850 € | ≤ 3 000 € | ✅ |
| **Latence API p95** | 185 ms | < 200 ms | ✅ |
| **Uptime API** | 99,8 % | ≥ 99,5 % | ✅ |

### Responsabilités Finales

| Membre | Contribution principale à ce document |
|---|---|
| **Djamel Chebbah** | Organisation agile · Rôles Scrum · KPIs · Pilotage prestataires · RACI |
| **Noé Wibaut** | Sprint Planning · Backlog · Jalons · Vue Sponsor |
| **Thuy-Trang Nguyen** | User Stories modélisation IA · Critères d'acceptation |
| **Paul-Henri Dourneau** | Cartographie ODRE/Météo-France · Procédures incidents |
| **Dorian Marty** | SLA techniques · Monitoring KPIs · Architecture MLOps |

---

*Document rédigé dans le cadre de la MSPR TPRE932 & TPRE942 – Référentiel RNCP36582 – Promotion 2025-2026.*  
*Date de rédaction : Juin 2026*
