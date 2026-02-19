from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.deps import get_db
from app.models.visit import Visit
from app.schemas.visit import WalkInCreate, VisitOut

router = APIRouter()

@router.post("/", response_model=VisitOut)
def create_walkin(payload: WalkInCreate, db: Session = Depends(get_db)):
    visit = Visit(
        visit_type="WALKIN",
        appointment_id=None,
        customer_name=payload.customer_name,
        phone=payload.phone,
        service_type=payload.service_type,
        arrival_time=datetime.utcnow(),
        status="WAITING"
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit
