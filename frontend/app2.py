import streamlit as st
import requests
from datetime import date
import math

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Home Credit Risk Predictor",
    page_icon="🏠",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"
today = date.today()

# ---------------------------
# Custom Styling
# ---------------------------
st.markdown("""
<style>
.main-title{
    font-size:42px;
    font-weight:bold;
    color:#1E3A8A;
}
.sub-text{
    color:gray;
    font-size:16px;
}
.result-box{
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-size:25px;
    font-weight:bold;
}
.low{
    background-color:#16A34A;
}
.medium{
    background-color:#F59E0B;
}
.high{
    background-color:#DC2626;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# EMI Calculator
# ---------------------------
def calculate_emi(principal, roi, tenure_years):

    monthly_rate = roi / (12 * 100)
    months = tenure_years * 12

    emi = (
        principal *
        monthly_rate *
        ((1 + monthly_rate) ** months)
    ) / (
        ((1 + monthly_rate) ** months) - 1
    )

    return emi

# ---------------------------
# Header
# ---------------------------
st.markdown(
    '<p class="main-title">🏠 Home Credit Risk Predictor</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-text">Predict customer home-loan repayment risk using Machine Learning</p>',
    unsafe_allow_html=True
)

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Personal Details",
        "Employment Details",
        "Loan Details",
        "Prediction"
    ]
)

# ---------------------------
# Session State
# ---------------------------
if "data" not in st.session_state:
    st.session_state.data = {}

# ===================================================
# PAGE 1 — PERSONAL DETAILS
# ===================================================
if page == "Personal Details":

    st.header("👤 Personal Details")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox(
            "Gender",
            ["M", "F"]
        )

        family_status = st.selectbox(
            "Family Status",
            [
                "Single / not married",
                "Married",
                "Civil marriage",
                "Separated",
                "Widow"
            ]
        )

        children = st.slider(
            "Number of Children",
            0,
            10,
            0
        )

    with col2:

        family_members = st.slider(
            "Family Members",
            1,
            15,
            2
        )

        housing = st.selectbox(
            "Housing Type",
            [
                "House / apartment",
                "Rented apartment",
                "Municipal apartment",
                "With parents",
                "Co-op apartment",
                "Office apartment"
            ]
        )

        dob = st.date_input(
            "Date of Birth",
            min_value=date(1950,1,1),
            max_value=today
        )

    days_birth = -(today - dob).days

    st.session_state.data.update({
        "CODE_GENDER": gender,
        "NAME_FAMILY_STATUS": family_status,
        "CNT_CHILDREN": children,
        "CNT_FAM_MEMBERS": float(family_members),
        "NAME_HOUSING_TYPE": housing,
        "DAYS_BIRTH": days_birth
    })

# ===================================================
# PAGE 2 — EMPLOYMENT
# ===================================================
elif page == "Employment Details":

    st.header("💼 Employment Details")

    col1, col2 = st.columns(2)

    with col1:

        income_type = st.selectbox(
            "Income Type",
            [
                "Working",
                "Commercial associate",
                "Pensioner",
                "State servant",
                "Student",
                "Unemployed"
            ]
        )

        occupation = st.selectbox(
            "Occupation",
            [
                "Laborers",
                "Sales staff",
                "Core staff",
                "Managers",
                "Drivers",
                "High skill tech staff",
                "Accountants",
                "Medicine staff",
                "Security staff",
                "Cooking staff",
                "Cleaning staff",
                "Private service staff",
                "Low-skill Laborers",
                "IT staff",
                "HR staff",
                "Realty agents"
            ]
        )

    with col2:

        organization = st.selectbox(
            "Organization Type",
            [
                "Business Entity Type 1",
                "Business Entity Type 2",
                "Business Entity Type 3",
                "Self-employed",
                "Government",
                "School",
                "Medicine",
                "Construction",
                "Bank",
                "Transport: type 4",
                "Industry: type 3",
                "Trade: type 7",
                "XNA"
            ]
        )

        employment_date = st.date_input(
            "Employment Start Date"
        )

        annual_income = st.number_input(
            "Annual Income",
            min_value=10000,
            value=300000
        )

    days_employed = -(
        today - employment_date
    ).days

    st.session_state.data.update({
        "NAME_INCOME_TYPE": income_type,
        "OCCUPATION_TYPE": occupation,
        "ORGANIZATION_TYPE": organization,
        "DAYS_EMPLOYED": days_employed,
        "AMT_INCOME_TOTAL": float(annual_income)
    })

# ===================================================
# PAGE 3 — LOAN DETAILS
# ===================================================
elif page == "Loan Details":

    st.header("🏦 Loan Details")

    col1, col2 = st.columns(2)

    with col1:

        contract_type = st.selectbox(
            "Contract Type",
            ["Cash loans","Revolving loans"]
        )

        own_car = st.radio(
            "Own Car?",
            ["Y","N"]
        )

        own_realty = st.radio(
            "Own Property?",
            ["Y","N"]
        )

    with col2:

        loan_amount = st.number_input(
            "Loan Amount",
            min_value=10000,
            value=500000
        )

        goods_price = st.number_input(
            "Property / Goods Price",
            min_value=10000,
            value=600000
        )

        roi = st.slider(
            "Interest Rate (%)",
            1.0,
            20.0,
            8.5
        )

        tenure = st.slider(
            "Loan Tenure (Years)",
            1,
            35,
            20
        )

    emi = calculate_emi(
        loan_amount,
        roi,
        tenure
    )

    st.info(
        f"Calculated EMI (Annuity): ₹ {emi:,.2f}"
    )

    st.session_state.data.update({
        "NAME_CONTRACT_TYPE": contract_type,
        "FLAG_OWN_CAR": own_car,
        "FLAG_OWN_REALTY": own_realty,
        "AMT_CREDIT": float(loan_amount),
        "AMT_ANNUITY": float(emi),
        "AMT_GOODS_PRICE": float(goods_price)
    })

# ===================================================
# PAGE 4 — PREDICTION
# ===================================================
elif page == "Prediction":

    st.header("📊 Risk Prediction")

    if st.button("Predict Risk"):

        try:

            response = requests.post(
                API_URL,
                json=st.session_state.data
            )

            result = response.json()

            risk_score = result["risk_score"]
            risk_level = result["risk_level"]

            st.success("Prediction Complete")

            if risk_level == "Low Risk":
                css_class = "low"

            elif risk_level == "Medium Risk":
                css_class = "medium"

            else:
                css_class = "high"

            st.markdown(
                f"""
                <div class="result-box {css_class}">
                Risk Score: {risk_score}%<br>
                {risk_level}
                </div>
                """,
                unsafe_allow_html=True
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "FastAPI server is not running."
            )