
# feature engineering 
import numpy as np
from sklearn.base import (BaseEstimator, TransformerMixin)


def group_organization(x):

    government = [
        "Government",
        "Police",
        "Military",
        "Security Ministries",
        "Postal",
        "School",
        "University",
        "Emergency",
        "Kindergarten",
        "Housing",
        "Security"
    ]

    healthcare = [
        "Medicine"
    ]

    business = [
        "Business Entity Type 1",
        "Business Entity Type 2",
        "Business Entity Type 3",
        "Self-employed",
        "Realtor",
        "Advertising",
        "Insurance",
        "Legal Services"
    ]

    trade_services = [
        "Trade: type 1",
        "Trade: type 2",
        "Trade: type 3",
        "Trade: type 4",
        "Trade: type 5",
        "Trade: type 6",
        "Trade: type 7",
        "Restaurant",
        "Hotel",
        "Services",
        "Cleaning"
    ]

    industrial = [
        "Construction",
        "Electricity",
        "Agriculture",
        "Industry: type 1",
        "Industry: type 2",
        "Industry: type 3",
        "Industry: type 4",
        "Industry: type 5",
        "Industry: type 6",
        "Industry: type 7",
        "Industry: type 8",
        "Industry: type 9",
        "Industry: type 10",
        "Industry: type 11",
        "Industry: type 12",
        "Industry: type 13"
    ]

    transport = [
        "Transport: type 1",
        "Transport: type 2",
        "Transport: type 3",
        "Transport: type 4"
    ]

    finance_telecom = [
        "Telecom",
        "Bank",
        "Mobile"
    ]

    if x in government:
        return "Government"

    elif x in healthcare:
        return "Healthcare"

    elif x in business:
        return "Business"

    elif x in trade_services:
        return "Trade_Service"

    elif x in industrial:
        return "Industrial"

    elif x in transport:
        return "Transport"

    elif x in finance_telecom:
        return "Finance_Telecom"

    elif x == "XNA":
        return "Unknown"

    else:
        return "Other"


def group_income_type(x):

    other = [
        "Unemployed",
        "Student",
        "Businessman",
        "Maternity leave"
    ]

    if x in other:
        return "Other"

    return x



class FeatureEngineering(
    BaseEstimator,
    TransformerMixin
):

    def fit(self, X, y=None):
        return self


    def transform(self, X):

        X = X.copy()

        # -------------------
        # Fix anomalies
        # -------------------

        X["DAYS_EMPLOYED"] = (
            X["DAYS_EMPLOYED"]
            .replace(365243, np.nan)
        )

        X["CODE_GENDER"] = (
            X["CODE_GENDER"]
            .replace("XNA", "F")
        )

        # -------------------
        # Feature Engineering
        # -------------------

        # Age in years
        X["AGE"] = (
            X["DAYS_BIRTH"].abs() / 365
        )

        # Employment years
        X["EMPLOYMENT_YEARS"] = (
            X["DAYS_EMPLOYED"].abs() / 365
        )

        # Loan burden
        X["CREDIT_INCOME_RATIO"] = (
            X["AMT_CREDIT"] /
            X["AMT_INCOME_TOTAL"]
        )

        # Family financial burden
        X["INCOME_PER_MEMBER"] = (
            X["AMT_INCOME_TOTAL"] /
            X["CNT_FAM_MEMBERS"]
        )

        # -------------------
        # Group categories
        # -------------------

        X["ORGANIZATION_TYPE"] = (
            X["ORGANIZATION_TYPE"]
            .apply(group_organization)
        )

        X["NAME_INCOME_TYPE"] = (
            X["NAME_INCOME_TYPE"]
            .apply(group_income_type)
        )
        
        X["EMI_INCOME_RATIO"] = (X["AMT_ANNUITY"] /X["AMT_INCOME_TOTAL"])

        # -------------------
        # Drop raw columns
        # -------------------

        X.drop(
            columns=[
                "DAYS_BIRTH",
                "DAYS_EMPLOYED"
            ],
            inplace=True
        )

        return X