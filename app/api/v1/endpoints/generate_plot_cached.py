from fastapi import APIRouter
from app.services.vanna_service import setup_vanna

router = APIRouter()

@router.post("/generate_plot_cached")
def generate_plot_cached(code: str, df: dict):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)
