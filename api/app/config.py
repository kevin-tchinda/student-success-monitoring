import os
from dotenv import load_dotenv

load_dotenv()  # Charge .env
class Config:
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
    MLFLOW_USERNAME = os.getenv("MLFLOW_USERNAME") 
    MLFLOW_PASSWORD = os.getenv("MLFLOW_PASSWORD")
    CLASSIFICATION_MODEL_NAME = os.getenv("CLASSIFICATION_MODEL_NAME", "Student_Success_Classifier")
    REGRESSION_MODEL_NAME = os.getenv("REGRESSION_MODEL_NAME", "Student_Success_Regression")
    MODEL_VERSION = os.getenv("MODEL_VERSION", "1")

config = Config()
