from sklearn.model_selection import train_test_split

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.feature_engineering import FeatureEngineering
from src.preprocessing import Preprocessor
from src.training import ModelTraining
from src.testing import ModelTesting
from src.save_load import SaveLoad

# Load Data

loader = DataLoader()

home_credit_df = loader.load_data()


# Clean Data
cleaner = DataCleaner(home_credit_df)

home_credit_df = cleaner.clean()


# Feature Engineering
feature_engineering = FeatureEngineering(home_credit_df)

home_credit_df = feature_engineering.transform()


# Split Features & Target

X = home_credit_df.drop(columns=["TARGET"])

y = home_credit_df["TARGET"]


# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# Fill Missing Values

numerical_columns = X_train.select_dtypes(include=["int64", "float64"]).columns

categorical_columns = X_train.select_dtypes(include=["object"]).columns


# Numerical Features
numerical_median = X_train[numerical_columns].median()

X_train[numerical_columns] = X_train[numerical_columns].fillna(numerical_median)

X_test[numerical_columns] = X_test[numerical_columns].fillna(numerical_median)


# Categorical Features
categorical_mode = X_train[categorical_columns].mode().iloc[0]

X_train[categorical_columns] = X_train[categorical_columns].fillna(categorical_mode)

X_test[categorical_columns] = X_test[categorical_columns].fillna(categorical_mode)

# Preprocessing

preprocessor = Preprocessor()

X_train_processed = preprocessor.fit_transform(X_train)

X_test_processed = preprocessor.transform(X_test)


# Save Processed Data

save_load = SaveLoad()

save_load.save_processed_data("X_train.pkl", X_train_processed)

save_load.save_processed_data("X_test.pkl", X_test_processed)

save_load.save_processed_data("y_train.pkl", y_train)

save_load.save_processed_data("y_test.pkl", y_test)

save_load.save("preprocessor.pkl", preprocessor)


# Train Model
trainer = ModelTraining()

model = trainer.random_forest(X_train_processed, y_train)


# Test Model
tester = ModelTesting(model, X_test_processed, y_test)

tester.evaluate()

# Save Model
save_load.save("random_forest.pkl", model)

print("\nTraining Completed Successfully.")
