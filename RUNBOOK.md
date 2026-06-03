# Runbook d'Exploitation Technique - EDF / RTE Predictor

Ce document décrit les procédures d'administration courante, de gestion des incidents et de rollback pour l'API de prédiction de consommation électrique nationale EDF/RTE.

---

## 1. Procédures d'Administration Courante

### A. Démarrer et Arrêter le Service (Kubernetes)
Le service s'exécute dans l'espace de noms (namespace) `edf-rte-production`.

* **Démarrer/Appliquer la configuration :**
  ```bash
  kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml -f k8s/hpa.yaml
  ```
* **Arrêter le service (supprimer le déploiement) :**
  ```bash
  kubectl delete -f k8s/deployment.yaml -f k8s/service.yaml -f k8s/hpa.yaml
  ```
* **Redémarrer les Pods (sans interruption - Rolling restart) :**
  ```bash
  kubectl rollout restart deployment/edf-consumption-predictor-api -n edf-rte-production
  ```

### B. Vérification de l'État de Santé (Healthchecks)
* **Lister les pods en cours d'exécution :**
  ```bash
  kubectl get pods -n edf-rte-production -l app=edf-consumption-predictor
  ```
* **Consulter les logs de l'API en temps réel :**
  ```bash
  kubectl logs -f deployment/edf-consumption-predictor-api -n edf-rte-production --tail=100
  ```
* **Vérifier l'état de l'Autoscaler (HPA) :**
  ```bash
  kubectl get hpa -n edf-rte-production
  ```
* **Tester la sonde de vie en HTTP :**
  ```bash
  curl http://<service-ip>/health
  ```
  *(Devrait renvoyer `{"status": "ok"}`)*

---

## 2. Déploiement & Procédure de Rollback Instantané

### A. Déployer une Nouvelle Version
Lorsqu'un nouveau commit est fusionné sur `main`, la CI/CD construit l'image Docker, la pousse avec le tag SHA du commit et met à jour Kubernetes.
Pour forcer manuellement la mise à jour avec une version spécifique de l'image :
```bash
kubectl set image deployment/edf-consumption-predictor-api predictor-api=edf-rte-registry.azurecr.io/predictor-api:v1.2.3 -n edf-rte-production
```

### B. Rollback en Cas d'Urgence (Retour arrière < 30 secondes)
Si une anomalie critique est détectée immédiatement après un déploiement (latences > 1s, taux d'erreur HTTP 500 élevé, prédictions aberrantes) :
1. **Lancer la commande de retour arrière :**
   ```bash
   kubectl rollout undo deployment/edf-consumption-predictor-api -n edf-rte-production
   ```
2. **Suivre le statut du rollback :**
   ```bash
   kubectl rollout status deployment/edf-consumption-predictor-api -n edf-rte-production
   ```
3. **Valider le bon retour à la normale :**
   Consulter le tableau de bord de supervision Grafana pour s'assurer que le taux d'erreur retombe à 0% et que les prédictions sont cohérentes.

---

## 3. Arbre de Résolution des Incidents Majeurs (Troubleshooting)

### Incident A : Pods en statut `OOMKilled` (Out Of Memory)
* **Symptômes :** Les pods s'arrêtent brutalement, le HPA recrée des conteneurs qui retombent aussitôt, code d'erreur K8s `Exit Code 137`.
* **Cause probable :** La taille des données chargées en mémoire pour l'inférence ou le calcul des métriques dépasse la limite configurée (512Mi).
* **Résolution :**
  1. Éditer le manifeste de déploiement [deployment.yaml](file:///c:/Users/Ph/Documents/Vscode/MSPR/k8s/deployment.yaml).
  2. Ajuster les ressources limites en doublant la mémoire allouée :
     ```yaml
     resources:
       requests:
         memory: "512Mi"
         cpu: "300m"
       limits:
         memory: "1Gi"
         cpu: "1000m"
     ```
  3. Appliquer la modification :
     ```bash
     kubectl apply -f k8s/deployment.yaml -n edf-rte-production
     ```

### Incident B : Alerte de Data Drift majeur détectée par Grafana
* **Symptômes :** Le dashboard Grafana affiche un indicateur "ROUGE" pour le drift thermique ou de charge.
* **Cause probable :** Changement de saison brutal (canicule précoce, vague de froid historique) rendant le modèle d'inférence obsolète.
* **Résolution :**
  1. Accéder à l'interface d'administration Apache Airflow.
  2. Sélectionner le DAG `edf_consumption_predictor_retraining`.
  3. Cliquer sur **Trigger DAG** pour lancer manuellement le ré-entraînement du modèle sur les 30 derniers jours de données réelles consommées.
  4. Suivre l'exécution jusqu'à la tâche finale `evaluate_and_compare`. Si le challenger est validé, il sera automatiquement promu en production.
  5. Si le drift persiste, contacter le Data Scientist d'astreinte pour ajouter des features climatiques spécifiques.

### Incident C : Erreur `503 Service Unavailable` sur `/predict`
* **Symptômes :** L'API répond avec un code HTTP 503 à chaque appel `/predict`.
* **Cause probable :** Le fichier de modèle `best_model.joblib` ou `data_pipeline.joblib` est corrompu ou manquant dans le répertoire `/app/models/`.
* **Résolution :**
  1. Entrer dans le conteneur pour inspecter les fichiers :
     ```bash
     kubectl exec -it <pod-name> -n edf-rte-production -- ls -la /app/models/
     ```
  2. Si le modèle est absent, déclencher manuellement la génération du modèle en exécutant la commande d'entraînement à l'intérieur du conteneur :
     ```bash
     kubectl exec -it <pod-name> -n edf-rte-production -- python -m src.models.train_evaluate
     ```
  3. Redémarrer le pod pour forcer le rechargement.

---

## 4. Rôles et Responsabilités MLOps

* **Surveillance quotidienne (Dashboards Grafana / Prometheus) :** Équipe d'infogérance EDF (Marc / Ops R&D).
* **Support Niveau 2 (Problèmes API / K8s) :** Ingénieur MLOps d'astreinte.
* **Support Niveau 3 (Précision du modèle / Drift statistique) :** Équipe Data Science R&D.
