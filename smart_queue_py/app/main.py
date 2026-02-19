from fastapi import FastAPI
from app.db.session import init_db
from app.api.routes import router as api_router

app = FastAPI(title="AI-Based Smart Queue & Appointment Management System")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(api_router, prefix="/api")
