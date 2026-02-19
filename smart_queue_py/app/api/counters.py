from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.counter import Counter
from app.core.config import settings
from app.schemas.counter import CounterOut

router = APIRouter()

@router.post("/seed", response_model=list[CounterOut])
def seed_counters(db: Session = Depends(get_db)):
    # Creates DEFAULT_COUNTERS if empty
    existing = db.query(Counter).count()
    if existing > 0:
        return db.query(Counter).order_by(Counter.counter_id).all()

    counters = []
    for i in range(1, settings.DEFAULT_COUNTERS + 1):
        c = Counter(counter_id=i, status="FREE", current_visit_id=None)
        db.add(c)
        counters.append(c)
    db.commit()
    return db.query(Counter).order_by(Counter.counter_id).all()

@router.get("/", response_model=list[CounterOut])
def list_counters(db: Session = Depends(get_db)):
    return db.query(Counter).order_by(Counter.counter_id).all()
