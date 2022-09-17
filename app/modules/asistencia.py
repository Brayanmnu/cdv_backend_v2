from fastapi import APIRouter
from pydantic import BaseModel
import app.utils as utils
from configs import get_values_database_sql

router = APIRouter(
    prefix="/asistencia",
    tags=["asistencia"])

host, port, db, usr, pwd = get_values_database_sql("database_pdn")

class Asistencia(BaseModel):
    id_maker_evento: str
    id_ponencia: str

@router.get("/maker-evento/{item_id}")
async def get_asistencias_by_maker_evento(item_id: str):
    try:
        conn = utils.conexion_postgres(host,port,db,usr,pwd)
        cursor = conn.cursor()
        select_query = "select p.id as nro_ponencia, concat(m.nombres,' ',m.apellidos)as nombres  from ponencia p inner join asistencia s on p.id=s.id_ponencia inner join maker_evento er on s.id_maker_evento = er.id inner join makerv2 m on er.id_makerv2=m.id_makerv2 where er.id=%s"
        cursor.execute(select_query,(item_id,))
        conn.commit()
        print('Query ejecutado')
        if cursor.rowcount > 0:
            records = cursor.fetchall()
            asistencias = []
            for row in records:
                json_asistencia = {
                    "nro_ponencia": row[0]
                }
                asistencias.append(json_asistencia)
                nombres = row[1]
            json_documento = {
                "nombres":nombres,
                "asistencias":asistencias
            }
    except Exception as error:
        print(f'Ocurrió un error inesperado: {error.__str__}')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('conexion terminada')
    return json_documento


@router.post("/registrar")
async def registrar_asistencia(asistencia: Asistencia):
    try:
        conn = utils.conexion_postgres(host,port,db,usr,pwd)
        cursor = conn.cursor()
        insert_asistencia = "insert into asistencia (id_maker_evento,id_ponencia) values (%s,%s)"
        cursor.execute(insert_asistencia,(asistencia.id_maker_evento,asistencia.id_ponencia))
        conn.commit()
        print('Asistencia registrada')
        dict_json = {"status":"insertado"}
    except Exception as error:
        dict_json = {"status": "error"}
        print(f'Ocurrió un error inesperado: {error.__str__}')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('conexion terminada')
    return dict_json
