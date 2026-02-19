import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import joblib
from pathlib import Path
import math

CSV_PATH = "data/synthetic_queue_appointment_dataset_1800.csv"
MODEL_PATH = "app/ml/models/wait_time_model.pkl"

df = pd.read_csv(CSV_PATH)

y = df["waiting_time_min"].astype(float)

# Features available at arrival/check-in time
X = df[
    ["day_of_week", "time_slot", "service_type", "is_walk_in", "staff_available", "expected_service_time_min"]
].copy()

cat_cols = ["time_slot", "service_type"]
num_cols = ["day_of_week", "is_walk_in", "staff_available", "expected_service_time_min"]

pre = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", "passthrough", num_cols),
    ]
)

model = RandomForestRegressor(
    n_estimators=400,
    random_state=42
)

pipe = Pipeline([("pre", pre), ("model", model)])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)

mae = mean_absolute_error(y_test, pred)
rmse = math.sqrt(mean_squared_error(y_test, pred))

print("\n=== Wait-Time Model Report ===")
print("MAE:", mae)
print("RMSE:", rmse)

Path("app/ml/models").mkdir(parents=True, exist_ok=True)
joblib.dump(pipe, MODEL_PATH)
print("✅ Saved:", MODEL_PATH)
