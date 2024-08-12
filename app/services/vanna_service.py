from vanna.remote import VannaDefault
import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv
from app.services.dbconfig import create_connection

load_dotenv()  # Carga las variables de entorno desde el archivo .env

def setup_vanna():
    api_key = os.getenv('VANNA_API_KEY')
    model = os.getenv('VANNA_MODEL')

    connection = create_connection()

    if connection is not None:
        vn = VannaDefault(api_key=api_key, model=model)
        try:
            conn_info = connection.get_dsn_parameters()
            vn.connect_to_postgres(host=conn_info['host'], dbname=conn_info['dbname'], user=conn_info['user'], password=db_password, port=conn_info['port'])
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
    print(f"Resultado de la consulta SQL: {result}")
    return result

def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)
