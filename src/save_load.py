import joblib

from src.config import Config


class SaveLoad:

    def __init__(self):

        self.model_path = Config.MODEL_PATH

        self.processed_data_path = Config.PROCESSED_DATA_PATH

    # save
    def save(self, file_name, obj):

        joblib.dump(obj, f"{self.model_path}/{file_name}")

        print(f"{file_name} saved successfully.")

    # load

    def load(self, file_name):

        return joblib.load(f"{self.model_path}/{file_name}")

    # Save Processed Data

    def save_processed_data(self, file_name, data):

        joblib.dump(data, f"{self.processed_data_path}/{file_name}")

        print(f"{file_name} saved successfully.")

    # Load Processed Data

    def load_processed_data(self, file_name):

        return joblib.load(f"{self.processed_data_path}/{file_name}")


