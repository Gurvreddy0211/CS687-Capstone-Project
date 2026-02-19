from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date as dt_date
from app.db.deps import get_db
from app.models.appointment import Appointment
from app.models.visit import Visit
from app.schemas.appointment import AppointmentCreate, AppointmentOut
from app.schemas.visit import VisitOut

router = APIRouter()

@router.post("/", response_model=AppointmentOut)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    appt = Appointment(
        customer_name=payload.customer_name,
        phone=payload.phone,
        service_type=payload.service_type,
        scheduled_time=payload.scheduled_time,
        status="SCHEDULED",
        reminder_sent=False
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

@router.get("/", response_model=list[AppointmentOut])
def list_appointments(
    date: dt_date | None = Query(default=None),
    db: Session = Depends(get_db)
):
    q = db.query(Appointment)
    if date:
        start = datetime.combine(date, datetime.min.time())
        end = start + timedelta(days=1)
        q = q.filter(Appointment.scheduled_time >= start, Appointment.scheduled_time < end)
    return q.order_by(Appointment.scheduled_time).all()

@router.post("/{appointment_id}/checkin")
def checkin_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.status != "SCHEDULED":
        raise HTTPException(status_code=400, detail=f"Cannot check-in appointment with status {appt.status}")

    appt.status = "CHECKED_IN"

    visit = Visit(
        visit_type="APPOINTMENT",
        appointment_id=appt.id,
        customer_name=appt.customer_name,
        phone=appt.phone,
        service_type=appt.service_type,
        arrival_time=datetime.utcnow(),
        status="WAITING"
    )
    db.add(visit)
    db.commit()
    db.refresh(appt)
    db.refresh(visit)

    return {"appointment": AppointmentOut.model_validate(appt), "visit": VisitOut.model_validate(visit)}
