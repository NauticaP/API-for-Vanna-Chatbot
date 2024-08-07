from fastapi import APIRouter
from app.services.vanna_service import setup_vanna

router = APIRouter()

@router.post("/generate_plotly_code_cached")
def generate_plotly_code_cached(question: str, sql: str, df: dict):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code
