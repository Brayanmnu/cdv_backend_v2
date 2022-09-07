import mysql.connector


def conexion_mysql(hst:str, db: str, usr:str, pwd:str):
    conn = mysql.connector.connect(host=hst,database=db, user=usr,password=pwd)
    print('Conexión realizada')
    return conn