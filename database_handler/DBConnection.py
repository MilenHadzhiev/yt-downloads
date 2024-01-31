import os
from functools import cached_property

import psycopg2


class DBConnection:

    def __init__(self):
        self.__connection = None

    @cached_property
    def connection(self):
        return self.__connection

    def execute(self, sql: str) -> None:
        self.connection.cursor().execute(sql)
        self.connection.commit()

    def query(self, sql: str) -> dict:
        cursor = self.connection.cursor()
        self.connection.commit()
        return cursor.fetchone()

    def __enter__(self, db_name: str, user: str, password: str, host: str, port: str):
        self.__connection = psycopg2.connect(
            os.environ.get('db_name', 'yt_downloads'),
            user=os.environ.get('user', 'postgres'),
            password=os.environ.get('password', 'postgres'),
            host=os.environ.get('host', 'localhost'),
            port=os.environ.get('port', 5432)
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()