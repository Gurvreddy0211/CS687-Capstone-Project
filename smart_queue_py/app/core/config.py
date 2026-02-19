from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URL: str = "sqlite:///./smart_queue.db"
    DEFAULT_COUNTERS: int = 5

settings = Settings()
