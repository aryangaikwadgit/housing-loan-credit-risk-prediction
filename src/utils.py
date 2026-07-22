import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    ConfusionMatrixDisplay,
)


class Utils:

    @staticmethod
    def classification_report(y_true, y_pred):

        print("\nClassification Report\n")

        print(classification_report(y_true, y_pred))

    @staticmethod
    def roc_auc_score(y_true, y_probability):

        score = roc_auc_score(y_true, y_probability)

        print(f"\nROC-AUC Score : {score:.4f}")

        return score

    @staticmethod
    def confusion_matrix(y_true, y_pred):

        cm = confusion_matrix(y_true, y_pred)

        print("\nConfusion Matrix\n")

        print(cm)

        return cm

    @staticmethod
    def plot_confusion_matrix(y_true, y_pred):

        disp = ConfusionMatrixDisplay.from_predictions(y_true, y_pred)

        plt.title("Confusion Matrix")

        plt.show()

    @staticmethod
    def print_risk_score(probability):

        print("\nSample Risk Scores\n")

        print(probability[:10] * 100)
