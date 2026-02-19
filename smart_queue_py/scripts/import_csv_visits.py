import sys
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, init_db
from app.models.visit import Visit

def to_dt(x):
    if pd.isna(x) or x is None or str(x).strip() == "":
        return None
    try:
        return pd.to_datetime(x).to_pydatetime()
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_csv_visits.py data/your_dataset.csv")
        sys.exit(1)

    path = sys.argv[1]
    df = pd.read_csv(path)

    # Update these mappings to your real CSV columns
    arrival_col = "arrival_time"
    start_col = "service_start_time"
    end_col = "service_end_time"
    service_col = "service_type"
    status_col = "visit_status"
    name_col = "customer_name" if "customer_name" in df.columns else None

    init_db()
    db: Session = SessionLocal()

    inserted = 0
    for _, r in df.iterrows():
        arrival = to_dt(r.get(arrival_col)) or datetime.utcnow()
        start = to_dt(r.get(start_col))
        end = to_dt(r.get(end_col))
        service_type = str(r.get(service_col, "General"))
        raw_status = str(r.get(status_col, "WAITING")).upper()

        status = raw_status if raw_status in ["WAITING", "SERVING", "COMPLETED", "CANCELLED"] else "WAITING"
        customer_name = str(r.get(name_col, "Unknown")) if name_col else "Unknown"

        v = Visit(
            visit_type="WALKIN",
            appointment_id=None,
            customer_name=customer_name,
            phone="",
            service_type=service_type,
            arrival_time=arrival,
            service_start_time=start,
            service_end_time=end,
            status=status
        )
        db.add(v)
        inserted += 1

    db.commit()
    db.close()
    print(f"✅ Imported {inserted} visits")

if __name__ == "__main__":
    main()
