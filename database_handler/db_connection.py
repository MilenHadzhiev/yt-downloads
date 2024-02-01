import logging
import os
from functools import cached_property
from typing import Optional, Union, Type, List

import psycopg2


class DBConnection:
    log = logging.getLogger('DBConnection')

    PY_SQL_TYPES_MAP = {
        int: 'INT',
        str: 'TEXT'
    }

    def __init__(self):
        self.__connection = None
        self.__db_name = None
        self.__cursor = None

    def __enter__(self):
        self.__db_name = os.environ.get('db_name', 'yt_downloads')
        self.__connection = psycopg2.connect(
            dbname=self.__db_name,
            user=os.environ.get('user', 'postgres'),
            password=os.environ.get('password', 'postgres'),
            host=os.environ.get('host', 'localhost'),
            port=os.environ.get('port', 5432)
        )
        self.__cursor = self.__connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    @cached_property
    def database_name(self):
        return self.__db_name

    @cached_property
    def connection(self):
        return self.__connection

    @cached_property
    def cursor(self):
        return self.__cursor

    def perform_safely(self, sql: str, expect_result: Optional[bool] = False) -> Union[Optional[tuple], Exception]:
        try:
            return self.query(sql) if expect_result else self.execute(sql)
        except Exception as e:
            self.log.error(e)
            return Exception(str(e))

    def execute(self, sql: str) -> None:
        self.cursor.execute(sql)
        self.connection.commit()

    def query(self, sql: str) -> List[tuple]:
        self.execute(sql)
        return self.cursor.fetchall()

    def insert(self, table: str, serialized_values: List[Union[str, int]]) -> None:
        self.execute(self._build_insert_sql(table, serialized_values))

    def add_foreign_key(self, table: str, table_to: str, foreign_key_column: str, column_type: Type[Union[int, str]]) -> None:
        self.execute(self.__build_add_foreign_key_sql(table, table_to, foreign_key_column, column_type))

    def _build_insert_sql(self, table, serialized_values: List[Union[str, int]]) -> str:
        values = f'values({[", ".join(serialized_values)]}'
        sql = f"""
            INSERT INTO {table} ({self._get_table_columns_for_insert(table)}) VALUES ({values});
        """
        return sql

    def _get_table_columns_for_insert(self, table_name: str) -> str:
        columns = self.query(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position ASC")
        columns = '(' + ', '.join([column[0] for column in columns]) + ')'
        print(columns)

    def __build_add_foreign_key_sql(self, table: str, table_to: str, foreign_key_column: str, column_type: Type[Union[int, str]]) -> str:
        return f"""
            ALTER TABLE {table}
                ADD COLUMN {foreign_key_column} {self.__convert_python_type_to_sql_type(column_type)}
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_{foreign_key_column}') THEN
                ALTER TABLE {table}
                    ADD CONSTRAINT fk_{foreign_key_column}
                    FOREIGN KEY ({foreign_key_column}) REFERENCES {table_to}({foreign_key_column});
            END IF;            
        """

    def __convert_python_type_to_sql_type(self, col_type: Type[Union[int, str]]) -> str:
        return self.PY_SQL_TYPES_MAP[col_type]


with DBConnection() as c:
    c.insert('video', [1, 2, 3])