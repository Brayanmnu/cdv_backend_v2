from configparser import ConfigParser

file = "config.ini"
config = ConfigParser()
config.read(file)

def get_values_database_sql(entorno):
    host = config[entorno]['host']
    port = config[entorno]['port']
    db = config[entorno]['db']
    usr = config[entorno]['usr']
    pwd = config[entorno]['pwd']
    return host, port, db, usr, pwd

def get_values_database_nosql_collection_qr(entorno):
    uri = config[entorno]['uri'] 
    database = config[entorno]['database'] 
    collection_qr = config[entorno]['collection_qr'] 
    return uri, database, collection_qr


def get_values_hosting():
    return config['hosting']['url_hosting'] 