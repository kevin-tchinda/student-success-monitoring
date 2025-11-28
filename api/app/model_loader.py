# api/app/model_loader.py
import os
import mlflow.pyfunc
import mlflow.sklearn
import pandas as pd
import numpy as np
from app.config import config

class MLflowModelClient:
    def __init__(self):
        self.classification_model = None
        self.regression_model = None
        self.preprocessor_minmax = None
        self.preprocessor_standardization = None
        self.models_loaded = False
        
    def load_models(self):
        """Charge les modèles ET preprocessors depuis MLflow"""
        try:
            os.environ['MLFLOW_TRACKING_USERNAME'] = config.MLFLOW_USERNAME
            os.environ['MLFLOW_TRACKING_PASSWORD'] = config.MLFLOW_PASSWORD
            mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
            
            # Charger les modèles
            self.classification_model = mlflow.pyfunc.load_model(
                f"models:/{config.CLASSIFICATION_MODEL_NAME}/{config.MODEL_VERSION}"
            )
            self.regression_model = mlflow.pyfunc.load_model(
                f"models:/{config.REGRESSION_MODEL_NAME}/{config.MODEL_VERSION}"
            )
            
            # Charger les preprocessors
            self.preprocessor_minmax = mlflow.sklearn.load_model(
                "models:/Student_Success_Preprocessor_MinMax/1"
            )
            self.preprocessor_standardization = mlflow.sklearn.load_model(
                "models:/Student_Success_Preprocessor_Standardization/1"
            )
            
            self.models_loaded = True
            print("Modèles et preprocessors chargés avec succès")
            return True
            
        except Exception as e:
            print(f"Erreur chargement modèles/preprocessors: {e}")
            self.models_loaded = False
            return False
    
    def _prepare_features(self, student_input):
        """Convertit StudentInput en DataFrame pour le preprocessor"""
        data = {
            'Gender': [student_input.gender],
            'Internet_Access_at_Home': [student_input.internet_access_at_home],
            'Extracurricular_Activities': [student_input.extracurricular_activities],
            'Parental_Education_Level': [student_input.parental_level_of_education],
            'Study_Hours_per_Week': [student_input.study_hours_per_week],
            'Attendance_Rate': [student_input.attendance_rate],
            'Past_Exam_Scores': [student_input.past_exam_scores]
        }
        return pd.DataFrame(data)
    
    def predict_classification(self, student_input):
        """Prédiction classification avec preprocessing automatique"""
        if not self.models_loaded:
            raise ValueError("Modèles non chargés")
        
        # Préparation des données
        raw_df = self._prepare_features(student_input)
        
        # Preprocessing avec MinMaxScaler
        processed_features = self.preprocessor_minmax.transform(raw_df)
        
        # Prédiction
        return self.classification_model.predict(processed_features)
    
    def predict_regression(self, student_input):
        """Prédiction regression avec preprocessing automatique"""
        if not self.models_loaded:
            raise ValueError("Modèles non chargés")
        
        # Préparation des données
        raw_df = self._prepare_features(student_input)
        
        # Preprocessing avec StandardScaler
        processed_features = self.preprocessor_standardization.transform(raw_df)
        
        # Prédiction
        return self.regression_model.predict(processed_features)

model_client = MLflowModelClient()
