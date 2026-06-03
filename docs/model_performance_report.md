# Rapport de Performance des Modèles d'IA (RTE/EDF)

Ce document présente l'évaluation comparative des 4 algorithmes entraînés sur les données de consommation électrique.

## Données de Test & d'Entraînement
* **Horizon d'évaluation :** 180 jours d'historique demi-horaire.
* **Méthodologie de split :** Séparation chronologique (80% entraînement, 20% test) pour simuler la production sans fuite de données futures.
* **Variables d'entrée :** Température, inertie thermique (moyennes glissantes 3h/6h), indicateurs calendaires (heure, mois, jour de la semaine, week-end, jours fériés), encodages cycliques sinus/cosinus, et lags temporels ($t-24\text{h}$, $t-48\text{h}$, $t-7\text{j}$).

## Résultats Comparatifs

| Modèle | R² Score | RMSE (MW) | MAPE | Accuracy (±5%) | Temps d'entraînement |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **DecisionTree** | 0.4712 | 3617.6 | 5.48% | 64.42% | 0.020 s |
| **RandomForest** | 0.5838 | 3209.2 | 4.87% | 67.97% | 0.064 s |
| **KNeighbors** **(Champion)** | 0.6011 | 3142.1 | 4.68% | 69.48% | 0.009 s |
| **RBFN** | -0.3613 | 5804.2 | 9.19% | 48.04% | 1.251 s |

## Analyse Métier & Choix de Production
Le modèle sélectionné pour la mise en production est **KNeighbors**.

1. **Précision métier (Accuracy ±5%) :** Il affiche un taux de réussite de **69.48%** de prédictions sous le seuil d'alerte critique de 5% d'écart.
2. **Robustesse et sur-apprentissage :** La différence de performance entre le train et le test a été maîtrisée par la régularisation (ex: profondeur des arbres limitée, Ridge pour la couche RBFN).
3. **Temps de calcul :** L'inférence s'exécute en moins de 10 ms, ce qui est parfait pour l'intégration de production dans l'API FastAPI et respecte la contrainte de latence sous charge.
