import numpy as np


class FeatureEngineering:

    def __init__(self, data):

        self.data = data.copy()

    # GROUP ORGANIZATION

    @staticmethod
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
            "Security",
        ]

        healthcare = ["Medicine"]

        business = [
            "Business Entity Type 1",
            "Business Entity Type 2",
            "Business Entity Type 3",
            "Self-employed",
            "Realtor",
            "Advertising",
            "Insurance",
            "Legal Services",
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
            "Cleaning",
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
            "Industry: type 13",
        ]

        transport = [
            "Transport: type 1",
            "Transport: type 2",
            "Transport: type 3",
            "Transport: type 4",
        ]

        finance_telecom = ["Telecom", "Bank", "Mobile"]

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

    # GROUP INCOME TYPE

    @staticmethod
    def group_income_type(x):

        other = ["Unemployed", "Student", "Businessman", "Maternity leave"]

        if x in other:
            return "Other"

        return x

    # AGE

    def create_age(self):

        self.data["AGE"] = self.data["DAYS_BIRTH"].abs() / 365

        return self

    # EMPLOYMENT YEARS

    def create_employment_years(self):

        self.data["EMPLOYMENT_YEARS"] = self.data["DAYS_EMPLOYED"].abs() / 365

        return self

    # CREDIT / INCOME

    def create_credit_income_ratio(self):

        self.data["CREDIT_INCOME_RATIO"] = (
            self.data["AMT_CREDIT"] / self.data["AMT_INCOME_TOTAL"]
        )

        return self

    # INCOME / FAMILY

    def create_income_per_member(self):

        self.data["INCOME_PER_MEMBER"] = (
            self.data["AMT_INCOME_TOTAL"] / self.data["CNT_FAM_MEMBERS"]
        )

        return self

    # EMI / INCOME

    def create_emi_income_ratio(self):

        self.data["EMI_INCOME_RATIO"] = (
            self.data["AMT_ANNUITY"] / self.data["AMT_INCOME_TOTAL"]
        )

        return self

    # GROUP CATEGORIES

    def group_categories(self):

        self.data["ORGANIZATION_TYPE"] = self.data["ORGANIZATION_TYPE"].apply(
            self.group_organization
        )

        self.data["NAME_INCOME_TYPE"] = self.data["NAME_INCOME_TYPE"].apply(
            self.group_income_type
        )

        return self

    #  DROP COLUMNS

    def drop_columns(self):

        self.data.drop(columns=["DAYS_BIRTH", "DAYS_EMPLOYED"], inplace=True)

        return self

    # COMPLETE FEATURE ENGINEERING

    def transform(self):

        (
            self.create_age()
            .create_employment_years()
            .create_credit_income_ratio()
            .create_income_per_member()
            .create_emi_income_ratio()
            .group_categories()
            .drop_columns()
        )

        return self.data
