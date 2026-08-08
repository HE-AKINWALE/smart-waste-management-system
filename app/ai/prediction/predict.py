import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "waste_prediction_model.pkl"
)


# Load trained model once
model = joblib.load(MODEL_PATH)


def predict_waste_fill(
    capacity: float,
    fill_level: float,
    previous_fill: float,
    days_since_collection: int
):

    data = pd.DataFrame(
        [[
            capacity,
            fill_level,
            previous_fill,
            days_since_collection
        ]],
        columns=[
            "capacity",
            "fill_level",
            "previous_fill",
            "days_since_collection"
        ]
    )

    prediction = model.predict(data)[0]

    return round(float(prediction), 2)