from fastapi import APIRouter
from pydantic import BaseModel
import app.utils as utils
from configs import get_values_database_sql

router = APIRouter(
    prefix="/login",
    tags=["login"])

host, port, db, usr, pwd = get_values_database_sql("database_pdn")

class Login(BaseModel):
    usuario: str
    password: str

@router.post("/")
async def login_load(login: Login):
    try:
        conn = utils.conexion_postgres(host,port,db,usr,pwd)
        cursor = conn.cursor()
        select_query = "select row_to_json(row) from (select count(1) as status from usuariov2 where usuario = %s and pwd = %s ) row"
        cursor.execute(select_query,(login.usuario, login.password))
        conn.commit()
        print('Query ejecutado')
        if cursor.rowcount > 0:
            dict_json = cursor.fetchone()
            dict_json = dict_json[0]
    except Exception as error:
        dict_json = {"status": "error"}
        print(f'Ocurrió un error inesperado: {error}')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('conexion terminada')
    return dict_json

