from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.visit import Visit
from app.models.counter import Counter
from app.services.queue_service import serve_next, finish_service

router = APIRouter()

def estimate_wait_minutes(position: int, avg_service_minutes: int = 7) -> int:
    return max(0, position) * avg_service_minutes

@router.get("/status")
def queue_status(db: Session = Depends(get_db)):
    waiting = db.query(Visit).filter(Visit.status == "WAITING").order_by(Visit.arrival_time).all()
    serving = db.query(Visit).filter(Visit.status == "SERVING").order_by(Visit.service_start_time).all()
    counters = db.query(Counter).order_by(Counter.counter_id).all()

    waiting_out = []
    for idx, v in enumerate(waiting):
        waiting_out.append({
            "id": v.id,
            "customer_name": v.customer_name,
            "visit_type": v.visit_type,
            "service_type": v.service_type,
            "arrival_time": v.arrival_time,
            "status": v.status,
            "position": idx + 1,
            "eta_minutes": estimate_wait_minutes(idx)
        })

    return {
        "counters": [{"counter_id": c.counter_id, "status": c.status, "current_visit_id": c.current_visit_id} for c in counters],
        "serving": [{"id": v.id, "customer_name": v.customer_name, "service_type": v.service_type, "service_start_time": v.service_start_time} for v in serving],
        "waiting": waiting_out,
        "totals": {"waiting": len(waiting), "serving": len(serving)}
    }

@router.post("/serve/{counter_id}")
def serve(counter_id: int, db: Session = Depends(get_db)):
    return serve_next(db, counter_id)

@router.post("/finish/{counter_id}")
def finish(counter_id: int, db: Session = Depends(get_db)):
    return finish_service(db, counter_id)
