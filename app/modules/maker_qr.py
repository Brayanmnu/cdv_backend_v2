from fastapi import APIRouter
import app.utils as utils
import base64
import qrcode
from os import remove
from pymongo import MongoClient
from configs import get_values_database_sql, get_values_database_nosql_collection_qr, get_values_hosting

router = APIRouter(
    prefix="/maker-qr",
    tags=["maker-qr"])

host, port, db, usr, pwd = get_values_database_sql("database_remote")

uri_qr, database_no_sql_qr, collection_db_qr = get_values_database_nosql_collection_qr("mongodb_pdn")

hosting = get_values_hosting()


@router.get("/{item_id}")
async def get_qr_by_id_maker(item_id: str):
    try:
        client_mongo = MongoClient(uri_qr)
        db_mongo = client_mongo[database_no_sql_qr]
        collection_qr = db_mongo[collection_db_qr]
        for qr_base64 in collection_qr.find({ "id_evento_maker": item_id}):
            nombres = qr_base64['nombres_apellidos']
            
            qr_base64= qr_base64['b64_string']
            qr_base64 = str(qr_base64)
            qr_base64 = qr_base64[2:-1]
        dict_json = {"status":"ok","codigo_qr": qr_base64, "nombres_apellidos":nombres} 
    except Exception as error:
        print(f'Ocurrió un error inesperado: {error}')
        dict_json = {"status": "error"}
    return dict_json
