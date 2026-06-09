import os

import mariadb


def get_db_connection():
    host = os.environ.get('MARIADB_HOST', 'localhost')
    port = int(os.environ.get('MARIADB_PORT', 3306))
    user = os.environ.get('MARIADB_USER', 'root')
    password = os.environ.get('MARIADB_PASSWORD', '')
    database = os.environ.get('MARIADB_DATABASE', 'messages_db')

    connection = mariadb.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )
    return connection
