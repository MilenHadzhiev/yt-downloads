import os
from functools import cached_property

import psycopg2


class DatabaseHandler:
    TABLES_MAP = {
        'user': 'User',
        'video': 'Video'
    }

    @cached_property
    def connection(self):
        return psycopg2.connect(
            database=os.environ.get('db_name', 'yt_downloads'),
            user=os.environ.get('user', 'postgres'),
            password=os.environ.get('pass', 'postgres'),
            host=os.environ.get("host", "localhost"),
            port=os.environ.get("port", 5432)
        )