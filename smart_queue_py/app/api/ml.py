from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
from pathlib import Path

router = APIRouter()

MODELS_DIR = Path(__file__).resolve().parents[1] / "ml" / "models"
NO_SHOW_MODEL = MODELS_DIR / "no_show_model.pkl"
WAIT_TIME_MODEL = MODELS_DIR / "wait_time_model.pkl"

class NoShowRequest(BaseModel):
    day_of_week: int
    time_slot: str
    service_type: str
    is_walk_in: int
    staff_available: int
    previous_no_shows: int

class WaitTimeRequest(BaseModel):
    day_of_week: int
    time_slot: str
    service_type: str
    is_walk_in: int
    staff_available: int
    expected_service_time_min: float

@router.post("/predict-no-show")
def predict_no_show(payload: NoShowRequest):
    if not NO_SHOW_MODEL.exists():
        raise HTTPException(status_code=400, detail="No-show model not trained yet")
    model = joblib.load(NO_SHOW_MODEL)

    X = [[
        payload.day_of_week,
        payload.time_slot,
        payload.service_type,
        payload.is_walk_in,
        payload.staff_available,
        payload.previous_no_shows
    ]]

    # Because we trained with a DataFrame-like structure, easiest is to pass dict
    import pandas as pd
    df = pd.DataFrame([payload.model_dump()])
    proba = float(model.predict_proba(df)[0][1])
    return {"no_show_probability": proba}

@router.post("/predict-wait-time")
def predict_wait_time(payload: WaitTimeRequest):
    if not WAIT_TIME_MODEL.exists():
        raise HTTPException(status_code=400, detail="Wait-time model not trained yet")
    model = joblib.load(WAIT_TIME_MODEL)

    import pandas as pd
    df = pd.DataFrame([payload.model_dump()])
    pred = float(model.predict(df)[0])
    return {"predicted_waiting_time_min": pred}
