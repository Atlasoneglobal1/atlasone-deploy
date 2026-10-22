from fastapi import FastAPI
from .health import router as health_router
from .routes import router as fallback_router

app = FastAPI(title="Atlas One POS Fallback")

app.include_router(health_router)
app.include_router(fallback_router)
