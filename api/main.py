# api/main.py
import sys
import os

# Ajouter le chemin actuel au path
sys.path.insert(0, os.path.dirname(__file__))

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.model_loader import model_client
from app.schemas import StudentInput, PredictionResponse, HealthResponse, ClassificationResponse, RegressionResponse
from app.config import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    _ = app  # Évite le warning
    success = model_client.load_models()
    if not success:
        raise RuntimeError("Impossible de charger les modèles MLflow")
    yield

app = FastAPI(
    title="Student Success Prediction API",
    description="API pour prédire la réussite étudiante (classification et regression)", 
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Allez sur /docs pour la documentation"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        models_loaded=model_client.models_loaded,
        classification_model=config.CLASSIFICATION_MODEL_NAME,
        regression_model=config.REGRESSION_MODEL_NAME
    )

# Dans main.py - remplacer l'ancien endpoint /predict
@app.post("/predict", response_model=PredictionResponse)
async def predict(student: StudentInput):  # ← StudentInput au lieu de StudentFeatures
    try:
        # Conversion automatique et prétraitement
        features = student.to_features()
        
        result = PredictionResponse(features_used=features)
        
        if student.prediction_type == "classification":
            prediction = model_client.predict_classification(features)
            result.classification = ClassificationResponse(
                prediction=int(prediction[0]),
                model_name=config.CLASSIFICATION_MODEL_NAME
            )
        elif student.prediction_type == "regression":
            prediction = model_client.predict_regression(features)
            result.regression = RegressionResponse(
                prediction=float(prediction[0]),
                model_name=config.REGRESSION_MODEL_NAME
            )
        else:
            raise HTTPException(status_code=400, detail="Type de prédiction invalide")
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
