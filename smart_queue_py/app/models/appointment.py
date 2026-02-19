from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    phone = Column(String, default="")
    service_type = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)

    status = Column(String, default="SCHEDULED")  # SCHEDULED, CHECKED_IN, NO_SHOW, CANCELLED, COMPLETED
    reminder_sent = Column(Boolean, default=False)
