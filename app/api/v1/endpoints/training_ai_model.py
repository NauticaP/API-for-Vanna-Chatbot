from fastapi import APIRouter
from app.services.vanna_service import setup_vanna

router = APIRouter()

@router.post("/training_ai_model")
def training_ai_model():
    vn = setup_vanna()
    vn.train(ddl="CREATE TABLE productos2 (id int primary key, productoName varchar(255), category varchar(255), price decimal(18,2), ranting decimal(18,2), numreviews int, stockquantity int, ciscount decimal(18,2), sales decimal(18,2), dateadded date);")
    vn.train(question="Muestrame detalle de los headphones", sql="SELECT * FROM productos2 WHERE productoname = 'Headphones'")
    vn.train(question="Muestra las laptops añadidas en fecha del 2023", sql="SELECT * FROM productos2 WHERE productname = 'Laptop' AND dateadded >= '2023-01-01' AND dateadded <= '2023-12-31';")
    vn.train(question="Muestra el producto mejor calificado por categoría", sql="SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY ranting DESC) AS rn FROM productos2) ranked WHERE rn = 1;")
