from pathlib import Path
import joblib

BASE = Path(__file__).resolve().parent
MODELS_DIR = BASE / "models"
MODELS_DIR.mkdir(exist_ok=True)

NO_SHOW_PATH = MODELS_DIR / "no_show_model.pkl"
WAIT_TIME_PATH = MODELS_DIR / "wait_time_model.pkl"

def load_model(path):
    if path.exists():
        return joblib.load(path)
    return None
