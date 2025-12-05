# Suivi de la réussite étudiante
---
# API de Prédiction de Réussite Étudiante*


## Description
API de prédiction développée avec FastAPI permettant d'évaluer la réussite étudiante via des modèles de machine learning. L'API supporte deux types de prédictions : classification (réussite/échec) et régression (score de performance).

## Installation et Exécution Locale

### Prérequis
- Python 3.12+
- pip

### Installation des Dépendances
```bash
cd api
pip install -r requirements.txt
```

### Lancement de l'API Locale
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
L'API sera accessible sur `http://localhost:8000`

### Documentation Interactive
Accédez à la documentation automatique : `http://localhost:8000/docs`

## Dockerisation

### Fichiers de Configuration
- **Dockerfile** : Définit l'environnement d'exécution et les commandes pour construire l'image Docker
- **requirements.txt** : Liste toutes les dépendances Python nécessaires au projet

### Construction de l'Image Docker
```bash
docker build -t student-success-monitoring-api .
```

### Exécution du Conteneur Local
```bash
docker run -p 8000:8000 student-success-monitoring-api
```

## Structure du Projet
```
student-success-monitoring/
├── api/                    # Code source de l'API
│   ├── main.py           # Point d'entrée FastAPI
│   ├── app/              # Modules de l'application
│   │   ├── __init__.py   # Initialisation du package
│   │   ├── config.py    # Configuration et variables d'environnement
│   │   ├── schemas.py   # Modèles de validation Pydantic
│   │   └── model_loader.py # Client MLflow pour les modèles
│   ├── journal_de_projet.md # Journal de développement
│   └── requirements.txt  # Dépendances Python
├── artifacts/            # Artifacts du projet
├── data/                # Données du projet
├── Dockerfile           # Configuration Docker
├── notebooks/           # Notebooks d'analyse
├── requirements.txt    # Dépendances globales
└── .env                # Variables d'environnement
```

## Accès à la Version en Ligne
L'API est déployée sur **Google Cloud Run** et accessible publiquement à l'adresse :

**URL de production** : https://student-success-api-964480752854.us-central1.run.app

### Liens Importants
- **Dépôt GitHub** : https://github.com/kevin-tchinda/student-success-monitoring
- **MLflow DagsHub** : https://dagshub.com/kevin-tchinda/student-success-monitoring.mlflow
- **Google Container Registry** : https://console.cloud.google.com/gcr/images/student-success-monitoring

### Endpoints Disponibles
- **GET /health** : Vérifie le statut de l'API et des modèles
- **POST /predict** : Effectue des prédictions (classification ou régression)

### Exemple de Requête
```bash
curl -X POST "https://student-success-api-964480752854.us-central1.run.app/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "internet_access_at_home": "Yes",
    "extracurricular_activities": "Yes",
    "parental_level_of_education": "Bachelors",
    "study_hours_per_week": 15,
    "attendance_rate": 85,
    "past_exam_scores": 75,
    "prediction_type": "classification"
  }'
```

## Déploiement Cloud Run

### Commandes Exécutées
```bash
docker build -t student-success-monitoring-api .
docker tag student-success-monitoring-api gcr.io/student-success-monitoring/student-success-monitoring-api
docker push gcr.io/student-success-monitoring/student-success-monitoring-api
gcloud run deploy student-success-api --image gcr.io/student-success-monitoring/student-success-monitoring-api --platform managed --region us-central1 --allow-unauthenticated
```

### Spécifications Techniques
- **Image Docker** : 1.5GB
- **Mémoire** : 1Gi
- **CPU** : 1
- **Région** : us-central1

## Problèmes Rencontrés et Solutions

### Problème de Port Cloud Run
*Problème* : Cloud Run utilise le port 8080 par défaut, alors que l'API était configurée pour le port 8000.

*Solution* : Adaptation du Dockerfile pour utiliser la variable d'environnement PORT
```dockerfile
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080}
```

### Intégration MLflow
*Problème* : Les modèles MLflow attendaient des données normalisées.

*Solution* : Sauvegarde et chargement des preprocesseurs depuis MLflow pour garantir la cohérence des prédictions.

### Variables d'Environnement
*Problème* : Le fichier .env était inaccessible lors de la construction Docker.

*Solution* : Ajustement des chemins et gestion des erreurs dans le Dockerfile.

### Facturation Google Cloud
*Problème* : Activation requise de la facturation pour les services Container Registry et Cloud Run.

*Solution* : Configuration d'un compte de facturation avec limite de budget.

## Commandes Utiles

### Développement
```bash
# Tests unitaires
pytest

# Formatage du code
black api/

# Vérification de qualité
pylint api/
```

### Déploiement
```bash
# Construction et publication
docker build -t student-success-monitoring-api .
docker tag student-success-monitoring-api gcr.io/student-success-monitoring/student-success-monitoring-api
docker push gcr.io/student-success-monitoring/student-success-monitoring-api

# Déploiement Cloud Run
gcloud run deploy student-success-api --image gcr.io/student-success-monitoring/student-success-monitoring-api --platform managed --region us-central1 --allow-unauthenticated
```

## Technologies Utilisées
- **FastAPI** : Framework web Python
- **Docker** : Conteneurisation
- **Google Cloud Run** : Plateforme de déploiement serverless
- **MLflow** : Gestion des modèles de machine learning
- **DagsHub** : Hébergement MLflow
- **Pydantic** : Validation des données

## Documentation Complémentaire
Veuillez vous reférer au journal de développement complet : `https://github.com/kevin-tchinda/student-success-monitoring/blob/kevin-tchinda/api/journal_de_projet.md`