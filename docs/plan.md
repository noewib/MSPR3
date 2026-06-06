# Spécifications de Projet & Cahier des Charges Enrichi
## Prédiction de Consommation Électrique (EDF / RTE)

---

## 1. Phase de Cadrage et Management Agile (Bloc 4)

Cette phase initiale vise à structurer le périmètre, l'organisation et la gouvernance du projet dans un écosystème international complexe (9 centres de R&D mondiaux d'EDF) en intégrant les contraintes de ressources, de délais (38 heures de préparation) et d'inclusion.

### Étape 1.1 : Analyse des besoins et parties prenantes
* **Objectif :** Cartographier l'écosystème du projet et s'assurer de l'alignement entre les besoins de RTE (Réseau de Transport d'Électricité) et les directions métiers d'EDF.
* **Stack Technologique :** Miro (Brainstorming et Story Mapping), Confluence (Base de connaissances centrale), Microsoft Lens.
* **Étapes à réaliser :**
    1.  **Matrice RACI & Cartographie des Acteurs :** Identifier les sponsors (Direction Innovation EDF), les Experts Métiers (Dispatcheurs RTE, Ingénieurs Prévisions), l'Équipe Projet (Data Engineers, Data Scientists, MLOps, Scrum Master) et les utilisateurs finaux.
    2.  **Rédaction des Personas Métiers :**
        * *Persona 1 :* Marc, 45 ans, Dispatcheur National chez RTE. Besoin : Une prédiction infra-journalière fiable pour arbitrer l'activation des centrales de réserve. Frustration : Le manque d'explicabilité des modèles "boîte noire".
        * *Persona 2 :* Léa, 29 ans, Analyste Mix Énergétique chez EDF. Besoin : Anticiper la charge journalière pour optimiser l'achat/vente d'électricité sur les marchés spot (EPEX SPOT).
    3.  **Spécification des Cas d'Usage :** Définir les horizons temporels de prédiction (J+1 à mailles horaires et demi-horaires) et les seuils de criticité des erreurs de prévision (sur-estimation = surcoût de stockage/production ; sous-estimation = risque de blackout).

### Étape 1.2 : Planification macro (WBS & Allocation des Ressources)
* **Objectif :** Structurer le projet en lots de travail clairs et quantifier l'effort financier, humain et technique.
* **Stack Technologique :** Jira Software, GanttProject, MS Excel / Google Sheets (Modélisation budgétaire).
* **Étapes à réaliser :**
    1.  **Création du WBS (Work Breakdown Structure) à 3 niveaux :**
        * *Lot 1 : Cadrage & Gouvernance* (Spécifications, Architecture, Charte inclusive).
        * *Lot 2 : Data & Modélisation* (Ingestion éco2mix, Feature Engineering, Entraînement des 4 modèles, Évaluation).
        * *Lot 3 : MLOps & Déploiement* (API FastAPI, Dockerisation, CI/CD, Orchestration Kubernetes, Load Testing).
        * *Lot 4 : Maintenabilité & Change* (Monitoring Drift, Airflow DAGs, Runbook, Formations, Restitution).
    2.  **Estimation des Charges (Méthode Planning Poker) :** Répartir les 38 heures d'effort de l'équipe (4 à 5 apprenants) en sous-tâches n'excédant pas 4 heures pour garantir la granularité du suivi.
    3.  **Budget Fictif de Fonctionnement :** Établir le coût total de possession (TCO) incluant les coûts de ressources humaines (TJM moyen de 500€/jour), les coûts Cloud de calcul (instances de calcul GPU/CPU managées) et de stockage de données historiques.

### Étape 1.3 : Mise en place de la gouvernance Agile
* **Objectif :** Piloter l'exécution du projet par la valeur, assurer la transparence et s'adapter rapidement aux blocages techniques.
* **Stack Technologique :** Jira Agile Boards, Slack / MS Teams (Intégrations Webhooks Jira), Planhat / Trello.
* **Étapes à réaliser :**
    1.  **Attribution des Rôles Scrum :** Nommer 1 Product Owner (garant du Backlog), 1 Scrum Master (facilitateur, gestion des bloqueurs) et 2 à 3 Développeurs/Data Scientists.
    2.  **Initialisation du Product Backlog :** Création des Epics majeurs et déclinaison en User Stories (US) structurées : *« En tant que [Persona], je veux [Fonctionnalité] afin de [Bénéfice métier] »*.
    3.  **Définition de la DoD (Definition of Done) :** Une US est validée si : Code review effectuée par un pair, Tests unitaires passés (>80% de couverture), Modèle enregistré sur MLflow avec ses métriques, Pas de vulnérabilité critique Docker détectée.
    4.  **Rituels Agiles :** Planifier des Sprints très courts (simulés à l'échelle du projet), des Daily Stands de 5 minutes et des revues de sprint pour mesurer la vélocité via des graphiques de Burn-down.

### Étape 1.4 : Stratégie d'inclusion et de collaboration internationale
* **Objectif :** Assurer la collaboration synchrone/asynchrone fluide entre les centres R&D mondiaux (France, Chine, USA, Italie, Allemagne, etc.) et garantir l'accessibilité numérique.
* **Stack Technologique :** MS Teams/Slack (Canaux dédiés), Goblin.tools (Aide à la décomposition cognitive), Krisp (Réduction de bruit et clarté audio), LanguageTool.
* **Étapes à réaliser :**
    1.  **Gouvernance Interculturelle et Fuseaux Horaires :** Établir des fenêtres de communication communes ("Core Hours" universelles 14h-16h Paris Time) et documenter de manière rigoureuse et centralisée en anglais technique pour éliminer la dépendance aux échanges synchrones.
    2.  **Plan d'Inclusion Handicap (Physique et Cognitif) :**
        * *Handicap visuel/Daltonisme :* Imposer des palettes de couleurs contrastées conformes aux normes WCAG 2.1 / RGAA pour tous les tableaux de bord Grafana et interfaces web (utilisation de thèmes accessibles comme *ColorBrewer*).
        * *Neuroatypies (TDAH, Autisme) :* Utilisation de l'outil Goblin.tools pour transformer des tâches complexes en sous-étapes simples, et aménagement de synthèses textuelles claires après chaque réunion orale.
        * *Handicap Auditif :* Activation systématique du sous-titrage automatique et en temps réel lors des points d'équipe internationaux sur Teams/Zoom.

---

## 2. Développement de la Solution IA (Partie Technique)

L'implémentation algorithmique doit répondre à des critères d'exécutabilité stricts en comparant quatre familles de modèles sur les données éco2mix de RTE.

### Étape 2.1 : Acquisition et préparation des données
* **Objectif :** Collecter, nettoyer et enrichir les données de consommation pour maximiser le pouvoir prédictif des modèles.
* **Stack Technologique :** Python 3.10+, Pandas, NumPy, Scikit-Learn (Preprocessing), Requests / Urllib (Incrémentation API RTE).
* **Étapes à réaliser :**
    1.  **Ingestion :** Développer un script de requêtage automatisé de l'API RTE-Eco2mix pour extraire l'historique de consommation nationale demi-horaire, complété par les données thermiques nationales (synop Météo-France).
    2.  **Nettoyage :** Traiter les valeurs manquantes (imputation par interpolation linéaire pour les trous de courte durée ou par la moyenne du même jour de la semaine à la même heure pour les pannes prolongées). Suppression ou correction des anomalies aberrantes (ex: pics hors-normes).
    3.  **Feature Engineering Temporel et Climatologique :**
        * Extraction des composantes calendaires : jour de la semaine, mois, heure, indicateur de week-end, indicateur de jour férié (via la bibliothèque `holidays`).
        * Encodage cyclique des variables périodiques (heures, mois) à l'aide des transformations sinus/cosinus :
            $$	ext{Hour\_sin} = \sin\left(rac{2\pi 	imes 	ext{Hour}}{24}
ight), \quad 	ext{Hour\_cos} = \cos\left(rac{2\pi 	imes 	ext{Hour}}{24}
ight)$$
        * Création de variables de décalage temporel (*Lag features*) : Consommation à $t-24	ext{h}$, $t-48	ext{h}$ et $t-1	ext{ semaine}$.
        * Calcul de moyennes mobiles glissantes (*Rolling metrics*) sur 3h et 6h de la température pour capter l'inertie thermique des bâtiments.
    4.  **Scaling :** Normalisation des caractéristiques continues à l'aide de `RobustScaler` ou `StandardScaler` pour ne pas pénaliser les algorithmes sensibles aux distances (KNN, RBF).

### Étape 2.2 : Sélection et entraînement des modèles
* **Objectif :** Entraîner et optimiser quatre familles d'algorithmes distinctes pour résoudre le problème de régression.
* **Stack Technologique :** Scikit-Learn, TensorFlow / Keras ou PyTorch (pour le réseau RBF).
* **Étapes à réaliser :**
    1.  **Arbre de Décision Simple (DecisionTreeRegressor) :** Entraînement d'un modèle de base. Limitation de la profondeur maximale (`max_depth`) pour éviter le surapprentissage (*overfitting*).
    2.  **Forêt Aléatoire (RandomForestRegressor) :** Implémentation d'un modèle d'ensemble par bagging. Optimisation des hyperparamètres via un `GridSearchCV` ou `RandomizedSearchCV` (nombre d'estimateurs, échantillonnage minimal par feuille).
    3.  **K-Plus Proches Voisins (KNeighborsRegressor) :** Configuration du modèle basé sur la distance d'Euclide ou de Manhattan. Recherche du nombre optimal de voisins ($k$) et pondération par la distance (`weights='distance'`).
    4.  **Réseau de Neurones à Fonction de Base Radiale (RBFN) :**
        * Puisque Scikit-Learn n'inclut pas de RBFN natif, concevoir une architecture personnalisée (en PyTorch/Keras ou via un pipeline combinant du clustering et une régression linéaire).
        * *Étape A :* Appliquer un algorithme K-Means sur les données d'entrée pour déterminer les $C$ centres des fonctions gaussiennes.
        * *Étape B :* Transformer les données en calculant la distance de chaque échantillon par rapport à ces centres via une fonction d'activation gaussienne :
            $$\phi(x) = \exp(-\gamma ||x - c_i||^2)$$
        * *Étape C :* Connecter la sortie de cette couche cachée RBF à une couche linéaire dense finale pour prédire la consommation globale.

### Étape 2.3 : Évaluation rigoureuse de la performance
* **Objectif :** Comparer scientifiquement les modèles selon des axes de précision métier et d'efficacité informatique.
* **Stack Technologique :** Scikit-Learn Metrics, MLflow Tracking (Suivi centralisé des métriques).
* **Étapes à réaliser :**
    1.  **Calcul exhaustif des indicateurs imposés :**
        * *R² Scoring (Coefficient de détermination) :* Évaluer la proportion de variance expliquée par le modèle.
        * *Accuracy (Précision adaptée) :* Pour un problème de régression, l'Accuracy doit être définie sous forme de seuil métier, par exemple le pourcentage de prédictions se situant à moins de $\pm 5\%$ de la valeur réelle constatée :
            $$	ext{Accuracy}_{\pm 5\%} = rac{1}{N} \sum_{i=1}^N \mathbb{I}\left( \left| rac{y_i - \hat{y}_i}{y_i} 
ight| \le 0.05 
ight)$$
        * *RMSE (Root Mean Squared Error) :* Mesurer l'erreur moyenne en accordant un poids plus important aux grandes erreurs (pénalisation des pics manqués).
        * *MAPE (Mean Absolute Percentage Error) :* Quantifier l'erreur en pourcentage par rapport à la charge réelle (indicateur très parlant pour la direction EDF).
        * *Temps d'apprentissage :* Mesurer le temps CPU/GPU requis pour l'ajustement complet du modèle (critère de scalabilité).
    2.  **Rapport de Synthèse MLflow :** Consigner toutes les itérations dans une interface unique pour générer la matrice finale de choix du modèle de production.

---

## 3. Préparation du Déploiement (Bloc 3)

Le passage du code expérimental (Notebook) à un service industriel résilient nécessite une architecture moderne orientée MLOps.

### Étape 3.1 : Conteneurisation et Architecture d'API
* **Objectif :** Encapsuler le modèle sélectionné et sa logique d'inférence dans un environnement standardisé, isolé et réutilisable.
* **Stack Technologique :** FastAPI, Docker, Kubernetes (Minikube ou cluster de test managé), Uvicorn.
* **Étapes à réaliser :**
    1.  **Développement de l'API avec FastAPI :** Créer un point de terminaison synchrone/asynchrone POST `/predict` acceptant un format JSON structuré (contenant les métadonnées de date, les prévisions de températures et les indicateurs calendaires) et retournant la charge électrique prédite associée à un score de confiance.
    2.  **Écriture du Dockerfile optimisé :** Utiliser un mécanisme de *multi-stage build* pour réduire le poids final de l'image de production (Image de base : `python:3.10-slim`). Installer uniquement les dépendances d'inférence (pas de packages de d'entraînement comme le GridSearch). Configurer un utilisateur non-root pour des raisons évidentes de sécurité système.
    3.  **Rédaction des manifestes Kubernetes (K8s) :**
        * `deployment.yaml` : Définir les stratégies de mise à jour (RollingUpdate pour garantir une disponibilité continue sans interruption de service).
        * `service.yaml` : Exposer l'application en interne du cluster via un composant de type *ClusterIP* ou *LoadBalancer*.
        * `hpa.yaml` (Horizontal Pod Autoscaler) : Configurer le redimensionnement automatique des instances d'API si la charge CPU globale dépasse les 70%.

### Étape 3.2 : Mise en place de la plateforme CI/CD
* **Objectif :** Automatiser les processus d'intégration du code, de test de sécurité et de déploiement continu sur le Cloud.
* **Stack Technologique :** GitHub Actions (ou GitLab CI), Docker Hub / Amazon ECR, Cloud Target (AWS EKS ou Azure AKS), Pytest, Trivy (Analyse des vulnérabilités).
* **Étapes à réaliser :**
    1.  **Pipeline d'Intégration Continue (CI) :** Déclenché à chaque Pull Request sur la branche principale.
        * *Stage 1 : Linting & Qualité :* Passage de `Flake8` ou `Black` et vérification des types avec `Mypy`.
        * *Stage 2 : Tests unitaires :* Exécution des scripts `Pytest` (validation des dimensions des matrices, présence des colonnes obligatoires).
        * *Stage 3 : Security Check :* Analyse du code source avec `Bandit` et analyse des failles des dépendances et de l'image Docker avec `Trivy`.
    2.  **Pipeline de Déploiement Continu (CD) :** Si les tests passent, l'image Docker est automatiquement construite, tagguée avec le SHA du commit Git, poussée vers le registre d'images (ECR/DockerHub), puis le déploiement sur Kubernetes est mis à jour (approche GitOps ou via des scripts de déploiement direct).

### Étape 3.3 : Simulation virtuelle à échelle réelle (Load Testing)
* **Objectif :** Valider la stabilité de l'API d'inférence face à une sollicitation intense représentative d'une utilisation nationale d'EDF.
* **Stack Technologique :** Locust (Outil de test de performance programmable en Python).
* **Étapes à réaliser :**
    1.  **Écriture du script de test Locust :** Définir des comportements utilisateurs réalistes simulant des dispatcheurs RTE et des applications automatisées internes d'EDF qui interrogent l'API à des fréquences cycliques régulières.
    2.  **Définition des scénarios de charge :**
        * *Test de charge nominal :* 100 utilisateurs simultanés effectuant 5 requêtes par seconde.
        * *Test de crête (Spike Test) :* Montée brutale à 1000 utilisateurs simultanés pour simuler le moment du rafraîchissement horaire des données d'éco2mix.
    3.  **Analyse des indicateurs de robustesse :** Suivre l'évolution du taux d'erreur (qui doit rester strictement égal à 0%), le temps de réponse moyen, et la latence au 95ème et 99ème percentile ($p95 < 200	ext{ms}$).

---

## 4. Maintenabilité et Documentation (Bloc 3)

Garantir le cycle de vie de la solution IA implique de prévoir la dérive naturelle des modèles et de formaliser l'exploitation opérationnelle.

### Étape 4.1 : Processus de Monitoring (Data & Model Drift)
* **Objectif :** Détecter en temps réel la perte de précision du modèle due aux changements climatiques ou structurels de consommation.
* **Stack Technologique :** Prometheus (Collecte de métriques temporelles), Grafana (Visualisation des alertes), Evidently AI ou Whylogs (Calcul du drift).
* **Étapes à réaliser :**
    1.  **Instrumentation de l'API :** Exposer un point de terminaison `/metrics` compatible avec Prometheus pour suivre le nombre total de requêtes, le temps d'inférence et les valeurs prédites.
    2.  **Calcul de la dérive (Data Drift) :** Mettre en place un script planifié (hebdomadaire) avec *Evidently AI* pour comparer la distribution des données de température et de consommation réelles entrantes avec le jeu de données d'entraînement initial (utilisation du test statistique de Kolmogorov-Smirnov).
    3.  **Création du Dashboard Grafana :** Concevoir une interface visuelle synthétisant la santé du système avec des indicateurs de type feux tricolores (Vert : Nominal, Orange : Dérive statistique détectée, Rouge : Précision insuffisante exigeant une coupure du modèle).

### Étape 4.2 : Cycle de ré-entraînement
* **Objectif :** Automatiser la mise à jour des paramètres du modèle pour intégrer les ruptures saisonnières (vagues de froid, canicules, changements d'habitudes de consommation).
* **Stack Technologique :** Apache Airflow ou Prefect.
* **Étapes à réaliser :**
    1.  **Modélisation du DAG (Directed Acyclic Graph) Airflow :**
        * *Task 1 :* Extraction des nouvelles données consolidées de RTE sur les 3 derniers mois.
        * *Task 2 :* Prétraitement et Feature Engineering automatique.
        * *Task 3 :* Ré-entraînement des hyperparamètres du modèle en conservant l'architecture validée.
        * *Task 4 :* Évaluation comparative (Modèle Champion vs Modèle Challenger).
    2.  **Stratégie de validation automatique :** Le modèle Challenger (ré-entraîné) ne remplace le modèle Champion en production que si son MAPE global est inférieur à celui du Champion sur un jeu de données de test récent, et s'il ne présente pas d'anomalies de prédiction sur les cas critiques.

### Étape 4.3 : Rédaction du Runbook Technique
* **Objectif :** Fournir aux équipes de production de l'infogérance d'EDF un manuel d'exploitation clair pour minimiser le MTTR (Mean Time To Repair).
* **Stack Technologique :** Markdown (Document `RUNBOOK.md` stocké à la racine du dépôt de code Git).
* **Étapes à réaliser :**
    1.  **Procédures d'administration courante :** Commandes exactes pour démarrer, arrêter et vérifier l'état de santé du service (`kubectl get pods`, `kubectl logs`).
    2.  **Arbre de résolution des incidents types (Troubleshooting) :**
        * *Incident A : Erreur OOMKilled (Out Of Memory) sur les pods de calcul.* Action : Augmenter les limites de ressources mémoire dans le manifeste K8s.
        * *Incident B : Data Drift majeur détecté par Grafana.* Action : Déclencher manuellement le DAG Airflow de ré-entraînement immédiat.
    3.  **Procédure de Rollback instantané :** Commande de secours pour revenir à la version précédente stable de l'image Docker en moins de 30 secondes en cas d'anomalie critique découverte après un déploiement :
        ```bash
        kubectl rollout undo deployment/edf-consumption-predictor-api
        ```

---

## 5. Accompagnement au Changement (Bloc 3 & 4)

L'excellence technique ne garantit pas le succès du projet sans une stratégie d'adoption par les équipes opérationnelles d'EDF.

### Étape 5.1 : Analyse d'impact sur les processus métiers
* **Objectif :** Comprendre comment l'intégration des prédictions basées sur l'IA modifie la prise de décision quotidienne.
* **Stack Technologique :** Lucidchart, Camunda BPMN (Modélisation de processus).
* **Étapes à réaliser :**
    1.  **Modélisation du processus "As-Is" (Existant) :** Décisions de régulation du réseau prises manuellement par les équipes à partir d'historiques simples extrapolés de façon linéaire sous Excel, générant une forte charge mentale et une réactivité limitée aux anomalies météorologiques.
    2.  **Modélisation du processus "To-Be" (Futur ciblé) :** Intégration de l'API IA directement dans les consoles de supervision. Les dispatcheurs reçoivent des alertes proactives de surcharge ou sous-charge avec un indice de probabilité, leur permettant de planifier les ordres de dispatching énergétique avec plusieurs heures d'avance.
    3.  **Plan de transition :** Identifier les leviers psychologiques pour réduire la résistance au changement (peur du remplacement par la machine, perte de contrôle).

### Étape 5.2 : Formation, Sensibilisation & Check-list d'IA Responsable
* **Objectif :** Transférer les compétences aux utilisateurs et imposer un cadre éthique et explicable d'utilisation de l'intelligence artificielle.
* **Stack Technologique :** MkDocs (Génération de site de documentation utilisateur), SHAP / LIME (Explicabilité).
* **Étapes à réaliser :**
    1.  **Création du Kit d'Explicabilité :** Développer un module visuel (intégrant des graphiques d'impact SHAP) montrant quelles caractéristiques (ex: la chute brutale de température prévue à Metz) ont le plus influencé la hausse de la courbe de consommation prédite.
    2.  **Conception du Manuel d'Utilisation :** Rédiger un guide vulgarisé expliquant la signification concrète des indicateurs d'erreur (comment interpréter un MAPE de 3% lors d'un pic hivernal).
    3.  **Check-list d'IA Responsable (Gouvernance éthique) :**
        * [ ] *Transparence :* Les utilisateurs finaux savent-ils si la prévision affichée provient d'un modèle statistique classique ou d'une IA ?
        * [ ] *Contrôle humain (Human-in-the-loop) :* Le système permet-il à l'opérateur RTE de surcharger manuellement la prédiction de l'IA s'il dispose d'une information terrain non modélisée (ex: grève nationale d'usine ou événement exceptionnel) ?
        * [ ] *Sûreté des données :* Aucune donnée nominative ou sensible liée aux clients finaux n'est ingérée (respect strict du RGPD, utilisation exclusive de données agrégées à l'échelle nationale ou régionale).

### Étape 5.3 : Amélioration continue via le Lean Management
* **Objectif :** Ancrer l'outil dans une boucle d'évolution itérative permanente basée sur les retours réels du terrain.
* **Stack Technologique :** Google Forms / Microsoft Forms (Feedback Loops), Trello (Boîte à idées partagée), Canevas A3.
* **Étapes à réaliser :**
    1.  **Mise en place d'une Boucle de Feedback Utilisateur :** Intégrer un bouton discret "Signaler une anomalie de prévision" dans l'interface de visualisation. Chaque signalement capture le contexte de données exact pour enrichir le prochain jeu de test du modèle.
    2.  **Rapport de Résolution de Problèmes A3 Lean :** Structurer l'analyse en cas d'écart majeur de performance (ex: si le modèle manque totalement un pic de consommation) : Déclaration du problème, Analyse des causes profondes (méthode des 5 Pourquoi), Actions correctives immédiates, Standardisation du nouveau processus.

---

## Livrables Finaux Attendus & Structure des Dossiers

Pour valider les compétences des deux blocs devant le jury d'évaluation, les livrables seront scindés en deux dossiers documentaires distincts et complémentaires :

### Dossier Spécifique - Bloc 3 (Industrialisation & Maintenabilité)
1.  **Document d'Architecture Technique :** Schéma complet de l'infrastructure Cloud (FastAPI, Docker, Kubernetes) et description des flux d'ingestion de données depuis RTE-Eco2mix.
2.  **Rapport de Performance IA et Validation des Modèles :** Analyse comparative des 4 algorithmes (R², Accuracy, RMSE, MAPE, temps CPU) et justification documentée du choix final pour la mise en production.
3.  **Pipeline CI/CD & Spécifications de Sécurité :** Captures d'écran et code source des workflows d'automatisation (GitHub Actions, tests Pytest, scans Trivy).
4.  **Rapport de Simulation Virtuelle et Tests de Charge :** Résultats des courbes de charge Locust (latences, taux d'erreur sous contrainte).
5.  **Runbook d'Exploitation Technique :** Manuel contenant les scripts de démarrage/arrêt, l'arbre de troubleshooting et le protocole de rollback K8s.
6.  **Plan d'Accompagnement au Changement Technique :** Analyse d'impact des processus métiers (BPMN As-Is / To-Be) et Kit d'Explicabilité (SHAP/LIME).

### Dossier Spécifique - Bloc 4 (Management de Projet & Gouvernance Agile)
1.  **Cahier des Charges Fonctionnel et Technique (CdC) :** Analyse du besoin initial, cartographie globale des parties prenantes, fiches complètes des Personas Métiers et matrice de criticité des prévisions.
2.  **Planification Macro et Budgétisation (WBS) :** Work Breakdown Structure complet à 3 niveaux accompagné de l'estimation de l'effort et de l'évaluation budgétaire du projet (coûts humains et d'infrastructure Cloud).
3.  **Product Backlog Agile :** Capture ou export complet du tableau de suivi Jira contenant les Epics, les User Stories rédigées, leurs critères d'acceptation et la Definition of Done.
4.  **Tableau de Bord des KPIs d'Agilité :** Suivi de l'avancement de l'équipe (graphiques de vélocité, Burn-down charts simulés).
5.  **Plan de Management Inclusive et de Collaboration Internationale :** Charte de communication asynchrone pour les 9 centres R&D mondiaux et livret d'aménagements ergonomiques pour l'accueil des différents profils de handicap.

---

## Préparation Stratégique des Épreuves Orales (Soutenances)

Le candidat doit se préparer à deux soutenances orales indépendantes et cloisonnées de **50 minutes chacune**, devant un binôme d'évaluateurs professionnels.

### Soutenance 1 : Évaluation du Bloc 3 (Durée : 50 minutes)
* **Positionnement du Candidat :** Posture d'Ingénieur Senior MLOps / Architecte Solution IA.
* **Répartition indicative du temps :**
    * *20 minutes :* Présentation de l'architecture, démonstration de l'API FastAPI conteneurisée, validation des tests de charge Locust, stratégie de monitoring du Data Drift et démonstration du mécanisme de Rollback opérationnel.
    * *30 minutes :* Échange technique approfondi avec le jury (justifications sur le choix de l'architecture, gestion de la sécurité des conteneurs, interprétation mathématique de la couche RBF).

### Soutenance 2 : Évaluation du Bloc 4 (Durée : 50 minutes)
* **Positionnement du Candidat :** Posture de Directeur de Projet IA / Scrum Master / Consultant Organisationnel.
* **Répartition indicative du temps :**
    * *20 minutes :* Présentation de la démarche de cadrage, démonstration de la gouvernance Scrum (Jira Backlog, gestion de la vélocité), explication des arbitrages budgétaires et soutenance détaillée du plan d'inclusion handicap et de synchronisation des centres R&D internationaux.
    * *30 minutes :* Échange avec le jury centré sur la gestion des risques humains, la conduite du changement auprès des dispatcheurs EDF et l'alignement stratégique de la solution avec la transition énergétique.
