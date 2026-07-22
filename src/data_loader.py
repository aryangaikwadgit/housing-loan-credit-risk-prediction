import pandas as pd

from sklearn.model_selection import train_test_split

from src.config import Config
from src.features import features


class DataLoader:

    def __init__(self):

        self.data = None

        self.X = None

        self.y = None

    def load_data(self):

        self.data = pd.read_csv(Config.DATA_PATH, usecols=features)

        return self.data

    def split_features_target(self):

        self.X = self.data.drop(columns=["TARGET"])

        self.y = self.data["TARGET"]

        return self.X, self.y

    def train_test_split_data(self, test_size, random_state):

        return train_test_split(
            self.X,
            self.y,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y,
        )
