# api/app/model_loader.py
import mlflow.pyfunc
import os
import pandas as pd  #
from app.config import config

class MLflowModelClient:
    def __init__(self):
        self.classification_model = None
        self.regression_model = None
        self.models_loaded = False
        
    def load_models(self):
        """Charge les deux modèles depuis MLflow"""
        try:
            # Configure l'authentification
            os.environ['MLFLOW_TRACKING_USERNAME'] = config.MLFLOW_USERNAME
            os.environ['MLFLOW_TRACKING_PASSWORD'] = config.MLFLOW_PASSWORD
            mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
            
            # Charge les deux modèles
            self.classification_model = mlflow.pyfunc.load_model(
                f"models:/{config.CLASSIFICATION_MODEL_NAME}/{config.MODEL_VERSION}"
            )
            self.regression_model = mlflow.pyfunc.load_model(
                f"models:/{config.REGRESSION_MODEL_NAME}/{config.MODEL_VERSION}"
            )
            
            self.models_loaded = True
            return True
            
        except Exception as e:
            print(f"Erreur chargement modèles: {e}")
            self.models_loaded = False
            return False
    
    def _create_dataframe(self, features):
        """Crée un DataFrame avec les noms de colonnes attendus par le modèle"""
        column_names = [
            'onehotencoder__Gender_Female', 'onehotencoder__Gender_Male',
            'onehotencoder__Internet_Access_at_Home_No', 'onehotencoder__Internet_Access_at_Home_Yes',
            'onehotencoder__Extracurricular_Activities_No', 'onehotencoder__Extracurricular_Activities_Yes',
            'ordinalencoder__Parental_Education_Level',
            'remainder__Study_Hours_per_Week',
            'remainder__Attendance_Rate',
            'remainder__Past_Exam_Scores'
        ]
        return pd.DataFrame([features], columns=column_names)
    
    def predict_classification(self, features):
        """Prédiction classification (0/1)"""
        if not self.models_loaded:
            raise ValueError("Modèles non chargés")
        df = self._create_dataframe(features)
        return self.classification_model.predict(df)
    
    def predict_regression(self, features):
        """Prédiction regression (valeur continue)"""
        if not self.models_loaded:
            raise ValueError("Modèles non chargés")
        df = self._create_dataframe(features)
        return self.regression_model.predict(df)

model_client = MLflowModelClient()
