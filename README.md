Dans le dossier contenant les codes faire ouvrir terminal, puis mettre les commandes suivantes (la première autorise votre windows a faire un venv)
1) Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process 
2) ..venv\Scripts\activate 
3) pip install -r requirements.txt
4) uvicorn src.api.app:app --reload

Pour démonstration pipeline : 
- Ouvrez un terminal PowerShell dans le dossier de votre projet.
- Exécutez le script d'automatisation powershell : 

.\simulate_cloud.ps1

Que fait ce script ?
Il compile le code dans un Conteneur Docker.
Il envoie ce conteneur à votre orchestrateur Kubernetes local.
Il demande à Kubernetes de faire tourner 2 répliques (2 serveurs API) en même temps.
Il ouvre la connexion vers http://localhost:8000 pour que vous puissiez faire la démonstration. (http://127.0.0.1:8000/#api)
