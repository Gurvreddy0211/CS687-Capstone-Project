from pydantic import BaseModel
from typing import Optional

class CounterOut(BaseModel):
    id: int
    counter_id: int
    status: str
    current_visit_id: Optional[int]

    class Config:
        from_attributes = True
