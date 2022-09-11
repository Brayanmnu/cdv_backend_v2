from fastapi import APIRouter
import app.utils as utils
from configs import get_values_database_sql
import json


router = APIRouter(
    prefix="/evento",
    tags=["evento"]
    )

host, port, db, usr, pwd = get_values_database_sql('database_pdn')

@router.get("/publicado")
async def get_evento_publicado():
    json_evento = ""
    try:
        conn = utils.conexion_postgres(host,port,db,usr,pwd)
        query = "SELECT id, descripcion FROM evento WHERE publicado=1 "
        cursor = conn.cursor()
        cursor.execute(query)
        print('Query evento ejecutado')
        records = cursor.fetchone()
        id = records[0]
        descripcion = records[1]
        query = "select cantidad-(select count(1) from makerv2 m ) as disponible from aforo"
        cursor.execute(query)
        print('Query aforo ejecutado')
        records = cursor.fetchone()
        disponible = records[0]
        json_evento = {
            "id":id,
            "descripcion":descripcion,
            "disponible": disponible
        }
    except Exception as error:
        print(f'Ocurrió un error inesperado{error.__str__}')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('conexion terminada')
    return json_evento