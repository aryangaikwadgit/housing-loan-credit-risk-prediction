from sklearn.ensemble import RandomForestClassifier
# from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression


class ModelTraining:

    def __init__(self):

        self.model = None

# Logistic Regression


    def logistic_regression(self, X_train, y_train):

        self.model = LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=42
        )

        self.model.fit(X_train, y_train)

        return self.model


# Random Forest


    def random_forest(self, X_train, y_train):

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_leaf=3,
            class_weight={0:1,1:4},
            random_state=42,
            n_jobs=-1,
        )

        self.model.fit(X_train, y_train)

        return self.model



# Weighted Random Forest


    def weighted_random_forest(self, X_train, y_train):

        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=12,
            min_samples_split=10,
            min_samples_leaf=5,
            class_weight={0: 1, 1: 4},
            random_state=42,
            n_jobs=-1,
        )

        self.model.fit(X_train, y_train)

        return self.model


# XGBoost
    

    def xgboost(self, X_train, y_train):

        self.model = XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            scale_pos_weight=11.8,
            eval_metric="auc",
            random_state=42,
        )

        self.model.fit(X_train, y_train)

        return self.model
