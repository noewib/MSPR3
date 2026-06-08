Dans le dossier contenant les codes faire ouvrir terminal, puis mettre les commandes suivantes (la première autorise votre windows a faire un venv)
1) Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process 
2) ..venv\Scripts\activate 
3) pip install -r requirements.txt
4) uvicorn src.api.app:app --reload
