from fastapi import APIRouter
from pydantic import BaseModel
import app.utils as utils
from configs import get_values_database_sql
import pywhatkit
from datetime import datetime
import time

router = APIRouter(
    prefix="/whatsapp-send-message",
    tags=["whatsapp-send-message"])

host, port, db, usr, pwd = get_values_database_sql("database_pdn")


class MensajeMasivo(BaseModel):
    msg: str

@router.post("/")
async def send_message(msgMasivo: MensajeMasivo):
    try:
        conn = utils.conexion_postgres(host,port,db,usr,pwd)
        query = "select concat(nombres,' ', apellidos) as maker, celular from makerv2 m where nro_doc ='47725593' or nro_doc ='75265962'"
        cursor = conn.cursor()
        cursor.execute(query)
        print('Query ejecutado')
        records = cursor.fetchall()
        dict_json = []
        for row in records:
            try:
                celular = row[1]
                celular = celular.replace("  ","")
                isCelularValido =False
                if celular[0:1] == '9' and len(celular)==9:
                    celular = "+51"+celular
                    isCelularValido = True
                elif celular[0:3] == '+51' and len(celular)==12:
                    isCelularValido = True

                if isCelularValido: 
                    print(f' maker: {row[0]} - celular:{celular}')
                    pywhatkit.sendwhatmsg_instantly(celular,msgMasivo.msg,15,True)
                    time.sleep(5) 
                    json_return ={
                        "status": "ok",
                        "nombre": row[0],
                        "celular": celular,
                    }
            except Exception as e:
                print(f'Ocurrió un error al enviar mensaje: {e} ')
                json_return ={
                    "status": "error",
                    "nombre": row[0],
                    "celular": celular,
                }
            dict_json.append(json_return)
    except Exception as error:
        print(f'Ocurrió un error en la conexión a bd: {error.__str__}')

    return dict_json