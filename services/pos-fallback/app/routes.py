from fastapi import APIRouter
from .fallback_logic import handle_pos_failure

router = APIRouter(prefix="/fallback")

@router.post("/pos-failure")
def pos_failure(payload: dict):
    return handle_pos_failure(payload)
