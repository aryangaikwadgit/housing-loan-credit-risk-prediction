from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd

from src.save_load import SaveLoad
from src.data_cleaner import DataCleaner
from src.feature_engineering import FeatureEngineering

app = FastAPI(title="Home Credit Risk Prediction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


save_load = SaveLoad()

model = save_load.load("random_forest.pkl")

preprocessor = save_load.load("preprocessor.pkl")


class CustomerData(BaseModel):

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


@app.get("/")
def home():

    return {"message": "Home Credit Risk Prediction API Running Successfully"}


@app.post("/predict")
def predict(customer: CustomerData):

    input_df = pd.DataFrame([customer.model_dump()])

    cleaner = DataCleaner(input_df)

    input_df = cleaner.clean()

    feature_engineering = FeatureEngineering(input_df)

    input_df = feature_engineering.transform()

    processed_input = preprocessor.transform(input_df)

    prediction = model.predict(processed_input)[0]

    probability = model.predict_proba(processed_input)[0][1]

    return {"prediction": int(prediction), "risk_score": round(probability * 100, 2)}
