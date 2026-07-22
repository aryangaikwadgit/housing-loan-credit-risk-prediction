from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score


class ModelTesting:

    def __init__(self, model, X_test, y_test):

        self.model = model

        self.X_test = X_test

        self.y_test = y_test

        self.y_pred = None

        self.y_probability = None

    # Prediction

    def predict(self):

        self.y_pred = self.model.predict(self.X_test)

        self.y_probability = self.model.predict_proba(self.X_test)[:, 1]

    # Classification Report

    def classification_report(self):

        print("\nClassification Report\n")

        print(classification_report(self.y_test, self.y_pred))

    # ROC AUC

    def roc_auc(self):

        score = roc_auc_score(self.y_test, self.y_probability)

        print(f"\nROC-AUC Score : {score:.4f}")

        return score

    # Confusion Matrix

    def confusion_matrix(self):

        cm = confusion_matrix(self.y_test, self.y_pred)

        print("\nConfusion Matrix\n")

        print(cm)

        return cm

    # Complete Evaluation

    def evaluate(self):

        self.predict()

        print("=" * 60)

        print("MODEL EVALUATION")

        print("=" * 60)

        self.classification_report()

        self.roc_auc()

        self.confusion_matrix()
