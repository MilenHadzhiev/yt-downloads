import os

import psycopg2


def get_conn_to_create_db():
    return psycopg2.connect(
        dbname='postgres',
        user=os.environ.get('user', 'postgres'),
        password=os.environ.get('password', 'postgres'),
        host=os.environ.get('host', 'localhost'),
        port=os.environ.get('port', 5432)
    )
