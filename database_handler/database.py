import os
from functools import cached_property
from typing import List, Union

import psycopg2
from database_handler.db_connection import DBConnection


class DatabaseHandler:
    """
    Interactions with PostgreSQL database should be handled here
    """

    def create_table(self, table_name, **kwargs) -> None:
        pass

    def insert(self, table_name: str, values: List[Union[int, str]]) -> None:
        pass

    def update(self, table_name: str, *args) -> None:
        pass

    def delete(self, table_name: str, *args) -> None:
        pass

    def get_result_dict(self, sql) -> dict:
        pass