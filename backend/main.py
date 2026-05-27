from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import sys

sys.path.append(r"C:\Main_Drive\work\workarea\projects\credit_risk_prediction\notebook")

import feature_engineering

# Create FastAPI app
app = FastAPI()


# Load trained model
model = joblib.load(
    r"C:\Main_Drive\work\workarea\projects\credit_risk_prediction\models\model_rf.pkl"
)

# Input schema
from pydantic import BaseModel


# Input Schema
class CustomerData(BaseModel):
    """Data Class"""

    NAME_CONTRACT_TYPE: str
    CODE_GENDER: str

    FLAG_OWN_CAR: str
    FLAG_OWN_REALTY: str

    CNT_CHILDREN: int

    AMT_INCOME_TOTAL: float
    AMT_CREDIT: float
    AMT_ANNUITY: float
    AMT_GOODS_PRICE: float

    NAME_INCOME_TYPE: str
    NAME_FAMILY_STATUS: str
    NAME_HOUSING_TYPE: str

    DAYS_BIRTH: int
    DAYS_EMPLOYED: int

    OCCUPATION_TYPE: str

    CNT_FAM_MEMBERS: float

    ORGANIZATION_TYPE: str


# Home Route
@app.get("/")
def home():
    return {"message": "Home Credit Risk API Running"}


# Prediction Route
@app.post("/predict")
def prediction(data: CustomerData):
    input_dict = data.dict()
    input_df = pd.DataFrame([input_dict])

    # Prediction
    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0]

    return {"risk_score": round(probability[1] * 100, 2)}
