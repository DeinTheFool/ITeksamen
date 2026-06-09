import pymysql
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def get_db_connection():
    connection = pymysql.connect(
        host=os.environ.get('MARIADB_HOST', 'localhost'),
        port=int(os.environ.get('MARIADB_PORT', 3306)),
        user=os.environ.get('MARIADB_USER', 'root'),
        password=os.environ.get('MARIADB_PASSWORD', ''),
        database=os.environ.get('MARIADB_DATABASE', 'messages_db'),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection