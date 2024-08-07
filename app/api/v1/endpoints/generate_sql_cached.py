from fastapi import APIRouter, JSONResponse
from pydantic import BaseModel
from app.services.vanna_service import setup_vanna, is_sql_valid_cached, run_sql_cached

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/generate_sql_cached")
def generate_sql_cached(question: QuestionRequest):
    vn = setup_vanna()
    sql = vn.generate_sql(question=question.question, allow_llm_to_see_data=True)
    
    if not is_sql_valid_cached(sql):
        return JSONResponse(status_code=400, content={"error": "Consulta SQL inválida"})

    response = run_sql_cached(sql)
    if response is None:
        return JSONResponse(status_code=500, content={"error": "Error al ejecutar la consulta SQL"})

    response_json = response.to_dict(orient="records")
    return JSONResponse(content={"data": response_json})
