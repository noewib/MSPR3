Write-Host "=== Lancement de la simulation Cloud (Kubernetes Local) ===" -ForegroundColor Cyan
Write-Host "1. Construction de l'image Docker locale..." -ForegroundColor Yellow
docker build -t predictor-api:local .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de la construction de l'image Docker. Assurez-vous que Docker Desktop est lance." -ForegroundColor Red
    exit 1
}

Write-Host "2. Deploiement sur le cluster Kubernetes local..." -ForegroundColor Yellow
kubectl apply -f k8s/local/deployment.yaml
kubectl apply -f k8s/local/service.yaml

Write-Host "3. Attente du demarrage des conteneurs (15 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 15
kubectl get pods

Write-Host "4. Redirection de port pour un acces immediat (Ctrl+C pour arreter)..." -ForegroundColor Yellow
Write-Host "L'API sera disponible sur : http://localhost:8000" -ForegroundColor Green
Write-Host "La documentation (Swagger) sera sur : http://localhost:8000/docs" -ForegroundColor Green
kubectl port-forward svc/edf-consumption-predictor-service-local 8000:8000
