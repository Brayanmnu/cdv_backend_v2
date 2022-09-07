from fastapi import APIRouter
import app.utils as utils
from configs import get_values_database_sql
import json


router = APIRouter(
    prefix="/tipo-documento",
    tags=["tipo-documento"]
    )

host, port, db, usr, pwd = get_values_database_sql('database_remote')

@router.get("/")
async def get_all_tipo_documento():
    dict_json = []
    try:
        conn = utils.conexion_mysql(host,db,usr,pwd)
        query = "SELECT  id_tipo_documento , descripcion from tipo_documento"
        cursor = conn.cursor()
        cursor.execute(query)
        print('Query ejecutado')
        records = cursor.fetchall()
        for row in records:
            json_documento = {
                "id":row[0],
                "descripcion":row[1]
            }
            dict_json.append(json_documento)
    except Exception as error:
        print(f'Ocurrió un error inesperado{error.__str__}')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('conexion terminada')
    return dict_json

