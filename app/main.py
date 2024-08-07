from fastapi import FastAPI
from app.api.v1.endpoints import generate_sql_cached, generate_plotly_code_cached, generate_plot_cached, generate_summary_cached, training_ai_model

app = FastAPI()

app.include_router(generate_sql_cached.router)
app.include_router(generate_plotly_code_cached.router)
app.include_router(generate_plot_cached.router)
app.include_router(generate_summary_cached.router)
app.include_router(training_ai_model.router)
