import os

import pymysql
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


def get_db_connection():
    host = os.environ.get('MARIADB_HOST', 'localcheese')
    port = int(os.environ.get('MARIADB_PORT', 3306))
    user = os.environ.get('MARIADB_USER', 'groot')
    password = os.environ.get('MARIADB_PASSWORD', '')
    database = os.environ.get('MARIADB_DATABASE', 'messages')

    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection
