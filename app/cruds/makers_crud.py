from fastapi import APIRouter
import app.utils as utils
from configs import get_values_database_sql
import json

router = APIRouter(
    prefix="/makers",
    tags=["makers"]
    )

host, port, db, usr, pwd = get_values_database_sql('database_remote')

@router.get("/")
async def get_all_makers():
    dict_json = []
    try:
        conn = utils.conexion_postgres(host,port,db,usr,pwd)
        query = "select row_to_json(row) from (select m.id_makerv2, me.id as id_maker_evento, m.nro_doc, m.nombres, m.apellidos, m.email, m.celular, m.fecha_creacion, m.fecha_actualizacion  from makerv2 m inner join maker_evento me on m.id_makerv2=me.id_makerv2 where m.estado=1 order by m.fecha_actualizacion desc) row"
        cursor = conn.cursor()
        cursor.execute(query)
        print('Query ejecutado')
        if cursor.rowcount > 0:
            records = cursor.fetchall()
            for row in records:
                dict_json.append(row[0])
    except Exception as error:
        print(f'Ocurrió un error inesperado{error.__str__}')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('conexion terminada')
    return dict_json

