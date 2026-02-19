from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.appointments import router as appointments_router
from app.api.walkins import router as walkins_router
from app.api.counters import router as counters_router
from app.api.queue import router as queue_router
from app.api.ml import router as ml_router

router = APIRouter()

router.include_router(health_router, tags=["health"])
router.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
router.include_router(walkins_router, prefix="/walkins", tags=["walkins"])
router.include_router(counters_router, prefix="/counters", tags=["counters"])
router.include_router(queue_router, prefix="/queue", tags=["queue"])
router.include_router(ml_router, prefix="/ml", tags=["ml"])