# api/app/schemas.py
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator

class StudentInput(BaseModel):
    gender: Literal["Male", "Female"] = Field(..., description="Genre de l'étudiant")
    internet_access_at_home: Literal["Yes", "No"] = Field(..., description="Accès Internet à la maison")
    extracurricular_activities: Literal["Yes", "No"] = Field(..., description="Activités extrascolaires")
    parental_level_of_education: Literal["High School", "Bachelors", "Masters", "PhD"] = Field(..., description="Niveau d'éducation parental")
    study_hours_per_week: float = Field(..., ge=0, le=168, description="Heures d'étude par semaine (0-168)")
    attendance_rate: float = Field(..., ge=0, le=100, description="Taux de présence (%)")
    past_exam_scores: float = Field(..., ge=0, le=100, description="Score aux examens précédents (0-100)")
    prediction_type: Literal["classification", "regression"] = Field("classification", description="Type de prédiction")
    
    @field_validator('study_hours_per_week')
    @classmethod
    def validate_study_hours_per_week(cls, v: float) -> float:
        """Valide les heures d'étude"""
        if v > 100:
            raise ValueError("Heures d'étude improbables (>100h/semaine)")
        return v
    
    def to_features(self) -> List[float]:
        """Convertit les données brutes en features pour le modèle"""
        # Encodage one-hot pour le genre
        gender_female = 1.0 if self.gender == "Female" else 0.0
        gender_male = 1.0 if self.gender == "Male" else 0.0
        
        # Encodage one-hot pour internet
        internet_access_at_home_no = 1.0 if self.internet_access_at_home == "No" else 0.0
        internet_access_at_home_yes = 1.0 if self.internet_access_at_home == "Yes" else 0.0
        
        # Encodage one-hot pour activités
        activities_no = 1.0 if self.extracurricular_activities == "No" else 0.0
        activities_yes = 1.0 if self.extracurricular_activities == "Yes" else 0.0
        
        # Encodage ordinal pour éducation parentale
        education_map = {"High School": 0.0, "Bachelors": 1.0, "Masters": 2.0, "PhD": 3.0}
        parental_education = education_map[self.parental_level_of_education]
        
        return [
            gender_female, gender_male,
            internet_access_at_home_no, internet_access_at_home_yes,
            activities_no, activities_yes,
            parental_education,
            self.study_hours_per_week,
            self.attendance_rate,
            self.past_exam_scores
        ]

class ClassificationResponse(BaseModel):
    prediction: int = Field(..., description="Classe prédite (0 ou 1)")
    model_name: str = Field(..., description="Nom du modèle de classification")

class RegressionResponse(BaseModel):
    prediction: float = Field(..., description="Valeur prédite (continue)")
    model_name: str = Field(..., description="Nom du modèle de regression")

class PredictionResponse(BaseModel):
    classification: Optional[ClassificationResponse] = None
    regression: Optional[RegressionResponse] = None
    features_used: List[float] = Field(..., description="Features après prétraitement")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Statut de l'API")
    models_loaded: bool = Field(..., description="Modèles chargés ou non")
    classification_model: str = Field(..., description="Nom modèle classification")
    regression_model: str = Field(..., description="Nom modèle regression")
