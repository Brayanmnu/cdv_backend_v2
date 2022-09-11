from fastapi import APIRouter
import app.utils as utils
from configs import get_values_database_sql,get_values_database_nosql_collection_qr, get_values_hosting
import json
from pydantic import BaseModel
import uuid
import qrcode
import base64
from os import remove
from pymongo import MongoClient
from typing import Optional


router = APIRouter(
    prefix="/registrar-maker",
    tags=["registrar-maker"]
    )

host, port, db, usr, pwd = get_values_database_sql('database_pdn')

uri_qr, database_no_sql_qr, collection_db_qr = get_values_database_nosql_collection_qr('mongodb_pdn')

hosting = get_values_hosting()

class Maker (BaseModel):
    id_tipo_doc: int
    nro_doc: str
    nombre: str
    apellido: str
    ciudad: Optional[str]
    edad: int
    iglesia: str
    celular: str
    email: Optional[str]
    id_evento: int


@router.post("/")
async def insert_maker(maker: Maker):
    try:
        
        conn = utils.conexion_postgres(host,port,db,usr,pwd)
        cursor = conn.cursor()
        query = "select count(1) from makerv2 m where nro_doc = %s"
        cursor.execute(query,(maker.nro_doc,))
        records = cursor.fetchone()
        cant_nro_doc = records[0]
        print(f'Query aforo ejecutado de disponibilidad: {cant_nro_doc}')

        if cant_nro_doc!=0:
            dict_json = {"status":"doc_repetido"}
        else:
            query = "select cantidad-(select count(1) from makerv2 m ) as disponible from aforo"
            
            cursor.execute(query)
            records = cursor.fetchone()
            disponible = records[0]
            print(f'Query aforo ejecutado de disponibilidad: {disponible}')
            
            
            if disponible>0:
                insert_maker = "insert into makerv2(id_tipo_doc,nro_doc,nombres,apellidos,email,celular,fecha_creacion,fecha_actualizacion) values(%s,%s,%s,%s,%s,%s,current_timestamp,current_timestamp)  RETURNING id_makerv2"
                cursor.execute(insert_maker,(maker.id_tipo_doc, maker.nro_doc, maker.nombre, maker.apellido, maker.email, maker.celular))
                conn.commit()
                print('Nuevo maker registrado')
                if cursor.rowcount > 0:
                    dict_json_maker = cursor.fetchone()
                    id_maker = dict_json_maker[0]

                    #Registrar a maker en evento
                    insert_evento_ciudad = "insert into maker_evento(id_makerv2,id_evento, ciudad, iglesia) values(%s,%s,%s,%s) RETURNING id"
                    cursor.execute(insert_evento_ciudad,(id_maker,maker.id_evento,maker.ciudad,maker.iglesia))
                    conn.commit()
                    print('Maker registrado a evento')
                    if cursor.rowcount > 0:
                        dict_json_evento = cursor.fetchone()
                        id_evento_maker = dict_json_evento[0]

                        nombres_apellidos = maker.nombre +" " +maker.apellido

                        #Generar codigoQR
                        url_qr = hosting
                        url_qr = str(url_qr)+ id_evento_maker
                        img = qrcode.make(url_qr)
                        print('qr generado correctamente')
                        img.save("qr_auxiliar.jpg")
                        with open("qr_auxiliar.jpg", "rb") as img_file:
                            b64_string = base64.b64encode(img_file.read())
                            b64_string = str(b64_string)
                        remove("qr_auxiliar.jpg")
                        client_mongo = MongoClient(uri_qr)
                        db_mongo = client_mongo[database_no_sql_qr]
                        collection_qr = db_mongo[collection_db_qr]
                        mydict = { "id_evento_maker": id_evento_maker, "b64_string": b64_string , "nombres_apellidos" : nombres_apellidos}
                        qr_result = collection_qr.insert_one(mydict)
                        print(f"Qr Guardado correctamente: {qr_result}")
                        client_mongo.close()

                        dict_json = {"status":"ok", "codigo_qr":b64_string[2:-1] , "nombres_apellidos" : nombres_apellidos}
            else:
                dict_json = {"status":"aforo"}
    except Exception as error:
        dict_json = {"status": "error"}
        print(f'Ocurrió un error inesperado,, cause: {error.__str__}')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print('conexion terminada')
    return dict_json