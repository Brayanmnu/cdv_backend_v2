from fastapi import APIRouter
import app.utils as utils
from configs import get_values_database_sql
import json


router = APIRouter(
    prefix="/evento",
    tags=["evento"]
    )

host, port, db, usr, pwd = get_values_database_sql('database_remote')

@router.get("/publicado")
async def get_evento_publicado():
    json_evento = ""
    try:
        conn = utils.conexion_postgres(host,port,db,usr,pwd)
        query = "SELECT id, descripcion FROM evento WHERE publicado=1 "
        cursor = conn.cursor()
        cursor.execute(query)
        print('Query ejecutado')
        records = cursor.fetchone()
        json_evento = {
            "id":records[0],
            "descripcion":records[1]
        }
    except Exception as error:
        print(f'Ocurrió un error inesperado{error.__str__}')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('conexion terminada')
    return json_evento

