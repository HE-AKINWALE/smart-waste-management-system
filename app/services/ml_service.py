from sklearn.linear_model import LinearRegression
import numpy as np

from sqlalchemy.orm import Session

from app.models.waste_bin import WasteBin


def predict_future_fill(bin_id: int, db: Session):

    waste_bin = (
        db.query(WasteBin)
        .filter(WasteBin.bin_id == bin_id)
        .first()
    )

    if not waste_bin:

        return {
            "predicted_fill_level": 0,
            "recommendation": "Waste bin not found."
        }

    # Example historical data
    days = np.array([
        1,
        2,
        3,
        4,
        5,
        6,
        7
    ]).reshape(-1, 1)

    fill_levels = np.array([
        15,
        25,
        40,
        52,
        66,
        80,
        waste_bin.fill_level
    ])

    model = LinearRegression()

    model.fit(days, fill_levels)

    prediction = model.predict([[8]])

    predicted_level = float(prediction[0])

    if predicted_level >= 90:

        recommendation = "Immediate waste collection required."

    elif predicted_level >= 75:

        recommendation = "Schedule collection within 24 hours."

    elif predicted_level >= 50:

        recommendation = "Monitor bin closely."

    else:

        recommendation = "Waste level is normal."

    return {

        "predicted_fill_level": round(predicted_level, 2),

        "recommendation": recommendation

    }