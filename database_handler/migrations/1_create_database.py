import os
from os.path import basename

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE


def migration():
    condition_sql = """
        SELECT 1 FROM pg_catalog.pg_database WHERE lower(datname) = lower('yt_downloads')
        """
    create_sql = """"
        CREATE DATABASE yt_downloads
    """
    connection = psycopg2.connect(
        dbname='postgres',
        user=os.environ.get('user', 'postgres'),
        password=os.environ.get('password', 'postgres'),
        host=os.environ.get('host', 'localhost'),
        port=os.environ.get('port', 5432)
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(condition_sql)
    if cursor.fetchone() is None:
        cursor.execute(create_sql)
    connection.close()
    print(f'Successfull migration {basename(__file__)}')

migration()

