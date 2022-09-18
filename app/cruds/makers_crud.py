from fastapi import APIRouter
import app.utils as utils
from configs import get_values_database_sql
import json

router = APIRouter(
    prefix="/makers",
    tags=["makers"]
    )

host, port, db, usr, pwd = get_values_database_sql('database_pdn')

@router.get("/{cant_registro}/{nro_pagina}")
async def get_makers(cant_registro: str,nro_pagina: str, nombre: str| None = None, apellido:str| None = None, nro_doc: str| None = None):
    dict_json = []
    try:
        filter = ""
        if nombre:
            filter = f"and UPPER(m.nombres) like '%{nombre}%' "
        if apellido:
            filter = filter + f"and UPPER(m.apellidos) like '%{apellido}%' "
        if nro_doc:
            filter = filter + f"and UPPER(m.apellidos) like '%{nro_doc}%' "
        
        conn = utils.conexion_postgres(host,port,db,usr,pwd)
        query = f"select  count(*) OVER() AS total_elements, m.id_makerv2, me.id as id_maker_evento, m.nro_doc, m.nombres, m.apellidos, m.email, m.celular, me.ciudad , me.iglesia, m.fecha_creacion, m.fecha_actualizacion  from makerv2 m inner join maker_evento me on m.id_makerv2=me.id_makerv2 where m.estado=1 {filter} order by m.fecha_actualizacion desc limit {cant_registro} offset {nro_pagina}"
        cursor = conn.cursor()
        cursor.execute(query)
        print('Query ejecutado')
        if cursor.rowcount > 0:
            records = cursor.fetchall()
            for row in records:
                query_cartilla = 'select count(1) from asistencia a2 where id_ponencia = 6';
                cursor.execute(query_cartilla)
                records_cartilla = cursor.fetchone()
                cant_cartillas = records_cartilla[0]

                query_asistencia = "select row_to_json(row) from (select p.id as nro_ponencia from  asistencia a inner join ponencia p on p.id = a.id_ponencia where a.id_maker_evento = %s) row"
                cursor.execute(query_asistencia,(row[2],))
                records_asistencia = cursor.fetchall()
                asistencias = []

                for row_asistencia in records_asistencia:
                    asistencias.append(row_asistencia[0])

                json_maker = {
                    'total_elements':row[0],
                    'id_makerv2':row[1],
                    'id_maker_evento': row[2],
                    'nro_doc': row[3],
                    'nombres': row[4],
                    'apellidos': row[5],
                    'email': row[6],
                    'celular': row[7],
                    'ciudad': row[8],
                    'iglesia': row[9],
                    'fecha_creacion': row[10],
                    'fecha_actualizacion': row[11],
                    'cant_cartillas': cant_cartillas,
                    'nro_asistencia': asistencias
                }
                dict_json.append(json_maker)
    except Exception as error:
        print(f'Ocurrió un error inesperado{error.__str__}')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('conexion terminada')
    return dict_json

