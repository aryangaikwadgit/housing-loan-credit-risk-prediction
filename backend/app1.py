from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app1 = FastAPI()

model = joblib.load(r"C:\Main_Drive\work\workarea\projects\credit_risk_prediction\models\homecredit_model.pkl")
features = joblib.load(r"C:\Main_Drive\work\workarea\projects\credit_risk_prediction\models\feature_columns.pkl")

class UserData(BaseModel):
    Cnt_Children: int
    Amt_Income_Total: float
    Amt_Credit: float
    Days_Birth: int
    Days_Employed: int
    Cnt_Fam_Members: float
    Days_Last_Phone_Change: float
    Flag_Own_Car2: int

@app1.get("/")
def home():
    return{
        "message":"Home Credit Risk API Running"
    }
    

@app1.post("/predict")
def prediction(data:UserData):
    input_dict = data.dict()

    input_df = pd.DataFrame([input_dict])

    for col in features:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[features]

    # Prediction
    prediction = model.predict(input_df)[0]

    probability = (model.predict_proba(input_df)[0])

    return {
        "risk_score": round(probability[1] * 100, 2)
    }

