from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WalkInCreate(BaseModel):
    customer_name: str
    phone: str = ""
    service_type: str

class VisitOut(BaseModel):
    id: int
    visit_type: str
    appointment_id: Optional[int]
    customer_name: str
    phone: str
    service_type: str
    arrival_time: datetime
    service_start_time: Optional[datetime]
    service_end_time: Optional[datetime]
    status: str

    class Config:
        from_attributes = True
