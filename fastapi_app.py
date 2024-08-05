from vanna.remote import VannaDefault
import psycopg2
from psycopg2 import OperationalError
import vanna as vn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# --------------------------------------------------
# Generamos las preguntas con la instancia de Vanna
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str

@app.get("/generate_questions_cached")
def generate_questions_cached():
    vn = setup_vanna()
    return vn.generate_questions()


@app.post("/training_ai_model")
def training_ai_model():
    vn = setup_vanna()
    vn.train(ddl="CREATE TABLE productos2 (id int primary key, productoName varchar(255), category varchar(255), price decimal(18,2), ranting decimal(18,2), numreviews int, stockquantity int, ciscount decimal(18,2), sales decimal(18,2), dateadded date);")
    vn.train(question="Muestrame detalle de los headphones",sql=f"""SELECT * FROM productos2 WHERE productoname = 'Headphones'""")
    vn.train(question="Muestra las laptops añadidas en fecha del 2023", sql=f"""SELECT * FROM productos2 WHERE productname = 'Laptop' AND dateadded >= '2023-01-01' AND dateadded <= '2023-12-31';""")
    vn.train(question="Muestra el producto mejor calificado por categoría", sql=f"""SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY ranting DESC) AS rn FROM productos2) ranked WHERE rn = 1;""")


@app.post("/generate_sql_cached")
def generate_sql_cached(question: str):
    vn = setup_vanna()
    sql = vn.generate_sql(question=question, allow_llm_to_see_data=True)
    
    if not is_sql_valid_cached(sql):
        return JSONResponse(status_code=400, content={"error": "Consulta SQL inválida"})

    response = run_sql_cached(sql)
    if response is None:
        return JSONResponse(status_code=500, content={"error": "Error al ejecutar la consulta SQL"})

    response_json = response.to_dict(orient="records")
    return JSONResponse(content={"data": response_json})

    

@app.post("/generate_plotly_code_cached")
def generate_plotly_code_cached(question, sql, df):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


@app.post("/generate_plot_cached")
def generate_plot_cached(code, df):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)


@app.get("/generate_summary_cached")
def generate_summary_cached(question, df):
    vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)

# -------------------------
# Generamos las funciones 
# -------------------------

def create_connection(db_name="db", db_user="user", db_password="password", db_host="host", db_port="port"):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def setup_vanna():
    api_key = 'Vanna API Key'
    model = 'Vanna Model'

    # Crea la conexion a la base de datos usando psycopg2
    connection = create_connection()

    if connection is not None:

        # Configuramos Vanna con la clave API y el modelo
        vn = VannaDefault(api_key=api_key, model=model)

        try:
            
            # Extrae los parámetros de la conexión para pasar a Vanna
            conn_info = connection.get_dsn_parameters()
            vn.connect_to_postgres(host=conn_info['host'], dbname=conn_info['dbname'], user=conn_info['user'], password='1234', port=conn_info['port'])
            print("Vanna connected successfully to the database")
            
        except Exception as e:
            print(f"Error connecting Vanna to the database: {e}")
        
        finally:
            connection.close()
        return vn
    
    else:
        print("Failed to connect to PostgreSQL. Vanna aborted.")
        return None


def is_sql_valid_cached(sql: str):
    vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)


def run_sql_cached(sql: str):
    vn = setup_vanna()
    result = vn.run_sql(sql=sql)
    print(f"Resultado de la consulta SQL: {result}")  # Imprime el resultado para depuración
    return result

def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)
