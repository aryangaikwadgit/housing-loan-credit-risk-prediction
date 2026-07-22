import pandas as pd


class DataCleaner:

    def __init__(self, data):

        self.data = data.copy()



    def remove_duplicates(self):

        self.data = self.data.drop_duplicates()

        return self



    def fix_gender(self):

        self.data["CODE_GENDER"] = (
            self.data["CODE_GENDER"]
            .replace("XNA", "F")
        )

        return self



    def fix_employment(self):

        self.data["DAYS_EMPLOYED"] = (
            self.data["DAYS_EMPLOYED"]
            .replace(365243, pd.NA)
        )

        return self



    def clean(self):

        (
            self
            .remove_duplicates()
            .fix_gender()
            .fix_employment()
        )

        return self.data