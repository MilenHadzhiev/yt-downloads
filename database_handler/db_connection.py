import logging
import os
from functools import cached_property
from typing import Optional, Union, Type, List, Tuple

import psycopg2


class DBConnection:
    """
    Context manager to execute sql queries
    """
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
        self.__db_name = os.environ.get('db_name')
        self.__connection = psycopg2.connect(
            dbname=self.__db_name,
            user=os.environ.get('user'),
            password=os.environ.get('password'),
            host=os.environ.get('host'),
            port=os.environ.get('port')
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

    def perform_safely(self, table_name: str, sql: str, expect_result: Optional[bool] = False) -> Union[Optional[tuple], Exception]:
        try:
            return self.query(table_name, sql) if expect_result else self.execute(sql)
        except Exception as e:  # pylint:disable=broad-exception-caught
            self.log.error(e)
            return Exception(str(e))

    def execute(self, sql: str) -> None:
        self.cursor.execute(sql)
        self.connection.commit()

    def query(self, table_name: str, sql: str) -> List[dict]:
        return self._build_response_dict(table_name, self.get_raw_response(sql))

    def get_raw_response(self, sql: str) -> List[tuple]:
        self.execute(sql)
        return self.cursor.fetchall()

    def _build_response_dict(self, table_name: str, result_values: List[Tuple[str]]) -> List[dict]:
        columns = self._get_table_columns(table_name)
        return [dict(pair) for pair in [zip(columns, res) for res in result_values]]

    def insert(self, table: str, serialized_values: List[Union[str, int]]) -> None:
        self.execute(self._build_insert_sql(table, serialized_values))

    def add_foreign_key(self, table: str, table_to: str, foreign_key_column: str, column_type: Type[Union[int, str]]) -> None:
        self.execute(self._build_add_foreign_key_sql(table, table_to, foreign_key_column, column_type))

    def _build_insert_sql(self, table, serialized_values: List[str | int]) -> str:
        values = f"""({", ".join([f"'{a}'" if not isinstance(a, (int, float)) else f'{a}' for a in serialized_values])})"""
        sql = f"""
            INSERT INTO {table}{self._get_table_columns_for_insert(table)} VALUES {values};
        """
        return sql

    def _get_table_columns_for_insert(self, table_name: str) -> str:
        return '(' + ', '.join(self._get_table_columns(table_name)) + ')'


    def _get_table_columns(self, table_name: str) -> List[str]:
        return [
            col[0] for col in self.get_raw_response(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position ASC"
            )
        ]

    def _build_add_foreign_key_sql(self, table: str, table_to: str, foreign_key_column: str, column_type: Type[Union[int, str]]) -> str:
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

    def __get_table_not_exists_sql(self, table_name: str) -> str:
        return f"""
                SELECT NOT EXISTS (
                    SELECT FROM
                        pg_tables
                    WHERE
                        schemaname = 'public' AND
                        tablename  = '{table_name}'
            )
            """

    def does_table_exist(self, table_name: str) -> bool:
        return self.get_raw_response(self.__get_table_not_exists_sql(table_name))[0][0]