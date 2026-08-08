from app.ai.prediction.predict import predict_waste_fill

from app.schemas.prediction_schema import (
    PredictionRequest
)


def waste_prediction(data: PredictionRequest):

    predicted_fill = predict_waste_fill(
        capacity=data.capacity,
        fill_level=data.fill_level,
        previous_fill=data.previous_fill,
        days_since_collection=data.days_since_collection
    )

    if predicted_fill >= 90:
        risk = "Critical"
        action = "Immediate Collection Required"

    elif predicted_fill >= 75:
        risk = "High"
        action = "Schedule Collection Soon"

    elif predicted_fill >= 50:
        risk = "Medium"
        action = "Continue Monitoring"

    else:
        risk = "Low"
        action = "No Immediate Action"

    return {
        "predicted_fill": predicted_fill,
        "risk_level": risk,
        "recommended_action": action
    }