from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):
    customer_name: str
    phone: str = ""
    service_type: str
    scheduled_time: datetime

class AppointmentOut(BaseModel):
    id: int
    customer_name: str
    phone: str
    service_type: str
    scheduled_time: datetime
    status: str
    reminder_sent: bool

    class Config:
        from_attributes = True
