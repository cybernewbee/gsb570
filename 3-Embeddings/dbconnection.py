import psycopg2
import os
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv(load_dotenv("/Users/marvinlee/Documents/vs_code/gsb_570/gsb570/3-Embeddings/.env"))

db_name = os.getenv('DBNAME')
db_user =  os.getenv('DBUSER')
db_password = os.getenv('PASSWORD')
db_host = os.getenv('HOST')
db_port = "5432"

def open_connection_to_db():
    # surround with try catch   
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
    except OperationalError as e:
        print(f"Error connecting to database: {e}")
        conn = None 

    return conn

def get_db_attributes():
    print(db_name, db_user, db_password, db_host, db_port)

def test_connection(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        print("Connection successful")
    except OperationalError as e:
        print(f"Error executing query: {e}")
    finally:
        if cur:
            cur.close()

def check_env():
    print(os.getenv('DBNAME'))
    print(os.getenv('DBUSER'))
    print(os.getenv('PASSWORD'))
    print(os.getenv('HOST'))
    print(os.getenv('PORT'))
    