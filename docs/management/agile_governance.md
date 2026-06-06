# Gouvernance Agile & Backlog Produit

Ce document décrit le cadre Scrum mis en place pour piloter le projet RTE / EDF et présente l'état de notre backlog.

---

## 1. Définition de la DoD (Definition of Done)

Pour valider chaque User Story (US) et l'intégrer au package livrable, les critères suivants doivent être respectés à 100% :

*   **Qualité du code :** Code revu par un pair, formaté avec `black` ou `ruff` sans aucune erreur de syntaxe ou d'importation.
*   **Qualité du typage :** Validation statique complète via `mypy`.
*   **Tests unitaires :** Taux de couverture de code minimum de **80%** (vérifié via `pytest-cov`).
*   **Modélisation :** Métriques d'entraînement et modèle enregistrés dans le registre local de modèles.
*   **Sécurité :** Scan de vulnérabilités Docker ou dépendances vierge de toute faille critique (via `Trivy` et `Bandit`).
*   **Documentation :** Code commenté et signatures typées, runbook ou guide d'exploitation mis à jour si modification de l'API.

---

## 2. Product Backlog (Epics & User Stories)

### EPIC 1 : Acquisition & Feature Engineering (Data)
#### US 1.1 : Ingestion automatique de la consommation RTE
*   **En tant qu'** Analyste Mix Énergétique,
*   **Je veux** récupérer automatiquement la consommation électrique nationale brute depuis l'API publique ODRE,
*   **Afin de** disposer d'un historique rafraîchi pour entraîner nos modèles de prévision.
*   *Critères d'acceptation :*
    *   Le script extrait les données nationales demi-horaires.
    *   Gestion automatique des pannes réseau ou API (basculement sur des données simulées de secours).

#### US 1.2 : Feature Engineering Temporel & Météo
*   **En tant que** Data Scientist,
*   **Je veux** enrichir les données de consommation brute avec des données thermiques et calendaires (lags, transformations sinus/cosinus, jours fériés),
*   **Afin d'** optimiser la pertinence prédictive de nos algorithmes.
*   *Critères d'acceptation :*
    *   Encodage trigonométrique des heures (1 à 24) et des mois (1 à 12).
    *   Calcul des décalages de charge ($t-24\text{h}$, $t-48\text{h}$, $t-7\text{j}$).
    *   Intégration automatique de la librairie `holidays` pour les jours fériés français.

---

### EPIC 2 : Modélisation Algorithmique (IA)
#### US 2.1 : Modèles Baselines (Arbre, Forêt, KNN)
*   **En tant que** Data Scientist,
*   **Je veux** entraîner des algorithmes d'Arbre de décision, de Forêt aléatoire et de K-Plus Proches Voisins optimisés par recherche d'hyperparamètres,
*   **Afin de** disposer de références de performance par rapport aux modèles plus complexes.
*   *Critères d'acceptation :*
    *   Optimisation des paramètres (profondeur, voisins, estimateurs).
    *   Exportation des métriques ($R^2$, RMSE, MAPE, Accuracy métier $\pm 5\%$).

#### US 2.2 : Réseau RBF (Radial Basis Function Network) Customisé
*   **En tant que** Data Scientist,
*   **Je veux** développer un réseau RBF personnalisé (KMeans + gaussiennes + régression linéaire),
*   **Afin de** capturer l'inertie thermique non linéaire et de le comparer aux modèles classiques.
*   *Critères d'acceptation :*
    *   Interface compatible scikit-learn (`fit`, `predict`).
    *   Évaluation comparative des 4 modèles.

---

### EPIC 3 : API & Infrastructure (MLOps)
#### US 3.1 : API d'inférence sécurisée avec FastAPI
*   **En tant que** Dispatcheur RTE,
*   **Je veux** envoyer des requêtes JSON sur un endpoint `/predict` et recevoir instantanément la prévision de charge,
*   **Afin d'** automatiser les arbitrages de dispatching depuis mon écran de contrôle.
*   *Critères d'acceptation :*
    *   Validation des schémas d'entrée avec Pydantic.
    *   Endpoint `/metrics` fournissant la latence et le volume pour Prometheus.
    *   Lancement sans privilège root dans un conteneur minimal.

#### US 3.2 : Intégration Continue (CI/CD) & Conteneurs
*   **En tant que** Développeur MLOps,
*   **Je veux** automatiser la validation du code et du conteneur dans GitHub Actions à chaque pull request,
*   **Afin de** prévenir le déploiement de régressions ou de failles de sécurité dans le cluster.
*   *Critères d'acceptation :*
    *   Pipeline automatisé avec Lint, Pytest et Scans Bandit/Trivy.

---

## 3. Simulation des Rituels & KPIs d'Agilité

### Sprint 1 : Fondations Data & IA (Heures 0 à 18)
*   **Objectif :** Valider l'ingestion, le feature engineering, et obtenir les métriques de performance des 4 modèles.
*   **Vélocité cible :** 24 Story Points (SP).
*   **Résultat :** 24 SP complétés.

### Sprint 2 : Industrialisation & Déploiement (Heures 18 à 38)
*   **Objectif :** Créer l'API FastAPI, la dockeriser, écrire les manifestes Kubernetes, configurer le monitoring et la CI/CD.
*   **Vélocité cible :** 26 Story Points (SP).
*   **Résultat :** 26 SP complétés.

### Burn-down Chart (Simulation d'avancement)

```
[Reste à Faire en Story Points]
50 | \
40 |  \
30 |   *----- (Fin Sprint 1 - Objectif Data/IA OK)
20 |         \
10 |          \
 0 +-----------* (Fin Sprint 2 - Déploiement & Monitoring OK)
   0h         18h         38h (Temps projet)
```
*   **Vélocité moyenne de l'équipe :** 25 SP par sprint.
*   **Bloqueurs identifiés et résolus :** La complexité de l'implémentation RBFN sans librairie tierce a nécessité un sprint planning révisé, compensé par l'utilisation d'une structure simplifiée s'appuyant sur le KMeans natif de scikit-learn.
