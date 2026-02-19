from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Counter(Base):
    __tablename__ = "counters"

    id = Column(Integer, primary_key=True, index=True)
    counter_id = Column(Integer, unique=True, nullable=False)

    status = Column(String, default="FREE")  # FREE, BUSY
    current_visit_id = Column(Integer, ForeignKey("visits.id"), nullable=True)
