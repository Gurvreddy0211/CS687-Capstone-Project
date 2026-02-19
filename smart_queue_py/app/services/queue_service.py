from datetime import datetime
from sqlalchemy.orm import Session
from app.models.visit import Visit
from app.models.counter import Counter

def compute_priority(visit: Visit) -> float:
    # FIFO base (older arrival first) but appointments get boost
    arrival_ms = visit.arrival_time.timestamp() * 1000
    score = -arrival_ms
    if visit.visit_type == "APPOINTMENT":
        score += 10_000_000_000  # strong boost
    # fairness boost: longer wait => higher score
    wait_minutes = max(0, (datetime.utcnow() - visit.arrival_time).total_seconds() / 60)
    score += min(wait_minutes, 120) * 10_000
    return score

def get_next_waiting_visit(db: Session) -> Visit | None:
    waiting = db.query(Visit).filter(Visit.status == "WAITING").all()
    if not waiting:
        return None
    waiting.sort(key=compute_priority, reverse=True)
    return waiting[0]

def serve_next(db: Session, counter_id: int):
    counter = db.query(Counter).filter(Counter.counter_id == counter_id).first()
    if not counter:
        raise ValueError("Counter not found")
    if counter.status == "BUSY":
        raise ValueError("Counter is BUSY")

    next_visit = get_next_waiting_visit(db)
    if not next_visit:
        return {"message": "No one in queue", "visit_id": None}

    next_visit.status = "SERVING"
    next_visit.service_start_time = datetime.utcnow()

    counter.status = "BUSY"
    counter.current_visit_id = next_visit.id

    db.commit()
    db.refresh(counter)
    db.refresh(next_visit)

    return {"message": "Serving started", "counter_id": counter.counter_id, "visit_id": next_visit.id}

def finish_service(db: Session, counter_id: int):
    counter = db.query(Counter).filter(Counter.counter_id == counter_id).first()
    if not counter:
        raise ValueError("Counter not found")

    if not counter.current_visit_id:
        counter.status = "FREE"
        db.commit()
        db.refresh(counter)
        return {"message": "Counter already free", "counter_id": counter.counter_id}

    visit = db.query(Visit).filter(Visit.id == counter.current_visit_id).first()
    if visit:
        visit.status = "COMPLETED"
        visit.service_end_time = datetime.utcnow()

    counter.status = "FREE"
    counter.current_visit_id = None

    db.commit()
    db.refresh(counter)
    if visit:
        db.refresh(visit)

    return {"message": "Service finished", "counter_id": counter.counter_id, "visit_id": visit.id if visit else None}
