from fastapi import APIRouter
from app.services.vanna_service import setup_vanna

router = APIRouter()

@router.get("/generate_summary_cached")
def generate_summary_cached(question: str, df: dict):
    vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)
