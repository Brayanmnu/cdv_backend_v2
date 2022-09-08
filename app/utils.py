import mysql.connector
import psycopg2

def conexion_postgres(host:str , port: str, db: str, usr:str, pwd:str):
    conn = psycopg2.connect(host=host, port=port, database=db, user=usr,password=pwd)
    print('Conexión realizada')
    return conn


def conexion_mysql(hst:str, db: str, usr:str, pwd:str):
    conn = mysql.connector.connect(host=hst,database=db, user=usr,password=pwd)
    print('Conexión realizada')
    return conn