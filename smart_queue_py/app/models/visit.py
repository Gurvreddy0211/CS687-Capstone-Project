from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.base import Base

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)

    visit_type = Column(String, nullable=False)  # WALKIN or APPOINTMENT
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)

    customer_name = Column(String, nullable=False)
    phone = Column(String, default="")
    service_type = Column(String, nullable=False)

    arrival_time = Column(DateTime, nullable=False)
    service_start_time = Column(DateTime, nullable=True)
    service_end_time = Column(DateTime, nullable=True)

    status = Column(String, default="WAITING")  # WAITING, SERVING, COMPLETED, CANCELLED
