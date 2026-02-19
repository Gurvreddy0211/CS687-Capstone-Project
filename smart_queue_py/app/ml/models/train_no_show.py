import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path

CSV_PATH = "data/synthetic_queue_appointment_dataset_1800.csv"
MODEL_PATH = "app/ml/models/no_show_model.pkl"

df = pd.read_csv(CSV_PATH)

# Target
y = df["no_show"].astype(int)

# Features (use only what is available before appointment time)
X = df[
    ["day_of_week", "time_slot", "service_type", "is_walk_in", "staff_available", "previous_no_shows"]
].copy()

cat_cols = ["time_slot", "service_type"]
num_cols = ["day_of_week", "is_walk_in", "staff_available", "previous_no_shows"]

pre = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", "passthrough", num_cols),
    ]
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

pipe = Pipeline([("pre", pre), ("model", model)])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipe.fit(X_train, y_train)

pred = pipe.predict(X_test)
proba = pipe.predict_proba(X_test)[:, 1]

print("\n=== No-Show Model Report ===")
print(classification_report(y_test, pred))
print("ROC-AUC:", roc_auc_score(y_test, proba))

Path("app/ml/models").mkdir(parents=True, exist_ok=True)
joblib.dump(pipe, MODEL_PATH)
print("✅ Saved:", MODEL_PATH)
