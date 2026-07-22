from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import OneHotEncoder, StandardScaler


class Preprocessor:

    def __init__(self):

        self.numerical_features = [
            "CNT_CHILDREN",
            "AMT_INCOME_TOTAL",
            "AMT_CREDIT",
            "AMT_ANNUITY",
            "AMT_GOODS_PRICE",
            "CNT_FAM_MEMBERS",
            "AGE",
            "EMPLOYMENT_YEARS",
            "CREDIT_INCOME_RATIO",
            "INCOME_PER_MEMBER",
            "EMI_INCOME_RATIO",
        ]

        self.categorical_features = [
            "NAME_CONTRACT_TYPE",
            "CODE_GENDER",
            "FLAG_OWN_CAR",
            "FLAG_OWN_REALTY",
            "NAME_INCOME_TYPE",
            "NAME_FAMILY_STATUS",
            "NAME_HOUSING_TYPE",
            "OCCUPATION_TYPE",
            "ORGANIZATION_TYPE",
        ]

        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), self.numerical_features),
                (
                    "cat",
                    OneHotEncoder(handle_unknown="ignore"),
                    self.categorical_features,
                ),
            ]
        )

    def fit(self, X_train):

        self.preprocessor.fit(X_train)

    def transform(self, X):

        return self.preprocessor.transform(X)

    def fit_transform(self, X_train):

        return self.preprocessor.fit_transform(X_train)

    def get_feature_names(self):

        return self.preprocessor.get_feature_names_out()
