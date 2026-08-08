import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# ----------------------------
# Locate dataset
# ----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "waste_data.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "waste_prediction_model.pkl"
)


# ----------------------------
# Load dataset
# ----------------------------

dataset = pd.read_csv(DATASET_PATH)

print("\nDataset Loaded Successfully\n")
print(dataset.head())


# ----------------------------
# Input and Output
# ----------------------------

X = dataset[
    [
        "capacity",
        "fill_level",
        "previous_fill",
        "days_since_collection"
    ]
]

y = dataset["predicted_fill"]


# ----------------------------
# Split dataset
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ----------------------------
# Train Model
# ----------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# ----------------------------
# Evaluate
# ----------------------------

prediction = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    prediction
)

score = r2_score(
    y_test,
    prediction
)

print("\nTraining Completed Successfully")

print(f"\nMean Absolute Error : {mae:.2f}")

print(f"R2 Score            : {score:.2f}")


# ----------------------------
# Save Model
# ----------------------------

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)

print("\nModel Saved Successfully")

print(MODEL_PATH)