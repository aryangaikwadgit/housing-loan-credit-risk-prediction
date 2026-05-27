import streamlit as st
import requests
from datetime import date
today = date.today()


API_URL = "http://127.0.0.1:8000/predict"

st.title("HOME CREDIT RISK PREDICTOR")

children = st.slider("Enter number of the children",0,10)

income = st.number_input("Enter annual income",1,10000000)

loan = st.number_input("Enter the loan amount",0,10000000)

dob = st.date_input("Enter DOB", min_value=date(1980, 1, 1),
    max_value=today)    
dob_in_days  = -(today - dob).days

doe = st.date_input("Employment Start Date")
employment_date =  -(today-doe).days

fam_mem = st.slider("number of family members",0,50)



date_last_phone = st.date_input("Enter date of last phone change")
days_last_phone_change = -(
    today - date_last_phone
).days


# own_car
car = st.radio("Do you own a Car?",["Yes","no"])
own_car = (
    1 if car.lower()=="yes"
    else 0
)

if st.button(
    "Predict Risk"
):

    data = {

        "Cnt_Children":
        children,

        "Amt_Income_Total":
        income,

        "Amt_Credit":
        loan,

        "Days_Birth":
        dob_in_days,

        "Days_Employed":
        employment_date,

        "Cnt_Fam_Members":
        float(fam_mem),

        "Days_Last_Phone_Change":
        float(
            days_last_phone_change
        ),

        "Flag_Own_Car2":
        own_car
    }

    try:
        
        response = requests.post(API_URL,json=data)
        result = response.json()

            

        st.success(f"The answer is: {result["risk_score"]}")


    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Make sure it's running.")