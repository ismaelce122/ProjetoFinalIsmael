import pymysql as my
from dotenv import load_dotenv
import os

load_dotenv()

def ConectarBanco():
    conexao = my.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME"),
        cursorclass = my.cursors.DictCursor 
    )
    return conexao