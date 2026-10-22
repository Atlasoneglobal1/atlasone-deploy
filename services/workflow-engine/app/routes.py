from fastapi import APIRouter
from .workflow_logic import handle_pos_failure, handle_ce_title_mortgage

router = APIRouter(prefix="/workflow")

@router.post("/pos-failure")
def pos_failure(payload: dict):
    return handle_pos_failure(payload)

@router.post("/ce-title-mortgage")
def ce_title_mortgage(payload: dict):
    return handle_ce_title_mortgage(payload)
