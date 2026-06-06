# Rapport de Performance des Modèles d'IA (RTE/EDF)

Ce document présente l'évaluation comparative des modèles entraînés sur les fichiers réels RTE Eco2mix.

## Données utilisées

* **Source :** fichiers RTE Eco2mix annuels définitifs + fichier consolidé, placés dans `data/raw`.
* **Période :** 2012-01-01 00:00:00 → 2026-01-31 00:00:00.
* **Données brutes après nettoyage :** 246960 lignes demi-horaires.
* **Données d'entraînement :** 5145 lignes journalières.
* **Cible :** consommation électrique moyenne journalière en MW (`target_consumption_mw`).
* **Température :** non utilisée, car elle n'est pas disponible dans les fichiers RTE fournis.
* **Variables d'entrée :** prévisions RTE J-1/J, variables calendaires, lags de consommation, moyennes glissantes, mix énergétique et taux de CO2.
* **Split :** séparation chronologique 80% entraînement / 20% test pour éviter la fuite de données futures.

## Résultats comparatifs

| Modèle | R² Score | RMSE (MW) | MAPE | Accuracy (±5%) | Temps d'entraînement |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **DecisionTree** | 0.9911 | 883.7 | 1.54% | 99.71% | 0.025 s |
| **RandomForest** **(Champion)** | 0.9929 | 789.9 | 1.42% | 99.90% | 0.290 s |
| **KNeighbors** | 0.9416 | 2266.3 | 3.26% | 79.30% | 0.000 s |
| **RBFN** | 0.9588 | 1903.5 | 2.78% | 84.16% | 0.034 s |


## Choix du modèle champion

Le modèle sélectionné est **RandomForest**, car il obtient le plus faible MAPE sur le jeu de test chronologique.

Le choix est fondé sur :
1. **MAPE**, pour mesurer l'erreur moyenne en pourcentage.
2. **RMSE**, pour mesurer l'erreur moyenne en MW.
3. **R²**, pour mesurer la capacité d'explication du modèle.
4. **Accuracy ±5%**, pour mesurer la proportion de prédictions dans un seuil métier acceptable.
5. **Temps d'entraînement**, pour vérifier la faisabilité du ré-entraînement.

## Artéfacts produits

* `models/best_model.joblib` : modèle champion.
* `models/data_pipeline.joblib` : pipeline de transformation.
* `models/mlflow_logs.json` : métriques des modèles.
* `models/training_metadata.json` : contexte d'entraînement.
* `models/test_predictions.csv` : prédictions sur le jeu de test.

