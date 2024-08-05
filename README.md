# API for Vanna-Chatbot with FastAPI

Este proyecto utiliza FastAPI para crear una API que interactúa con una base de datos PostgreSQL y la biblioteca Vanna para generar preguntas, entrenar modelos, generar consultas SQL, y más.

## Requisitos

Asegúrate de tener instaladas las siguientes librerías:

- `vanna`
- `psycopg2`
- `fastapi`
- `uvicorn`
- `pandas`
- `numpy`
- `pydantic`

Puedes instalarlas usando el archivo `requirements.txt` proporcionado:

```bash
pip install -r requirements.txt
```

## Cómo usar

1. Instalar dependencias.

2. Ejecutar la aplicación FastAPI:

```bash
uvicorn fastapi_app:app --reload
```
Esto iniciará el servidor en http://127.0.0.1:8000.

3. Endpoints disponibles:

- GET /generate_questions_cached: Genera preguntas usando Vanna.
- POST /training_ai_model: Entrena el modelo AI de Vanna.
- POST /generate_sql_cached: Genera una consulta SQL a partir de una pregunta.
- POST /generate_plotly_code_cached: Genera código Plotly a partir de una pregunta, consulta SQL y dataframe.
- POST /generate_plot_cached: Genera una gráfica Plotly a partir del código y dataframe.
- GET /generate_summary_cached: Genera un resumen a partir de una pregunta y dataframe.

4. Configuración de la base de datos:
Asegúrate de configurar correctamente los parámetros de conexión a la base de datos en la función create_connection.

## Notas

- Reemplaza 'Vanna API Key' y 'Vanna Model' en la función setup_vanna con tus valores reales.
- Asegúrate de que la base de datos PostgreSQL esté en funcionamiento y accesible con las credenciales proporcionadas.
