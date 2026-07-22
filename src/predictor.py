import pandas as pd


class Predictor:

    def __init__(self, model, preprocessor):

        self.model = model

        self.preprocessor = preprocessor



    def preprocess(self, data):

        if isinstance(data, dict):

            data = pd.DataFrame([data])

        return self.preprocessor.transform(data)


    def predict(self, data):

        processed_data = self.preprocess(data)

        prediction = self.model.predict(processed_data)[0]

        probability = self.model.predict_proba(processed_data)[0][1]

        return {
            "prediction": int(prediction),
            "risk_score": round(probability * 100, 2),
        }
