from os.path import basename

from database_handler.db_connection import DBConnection

def safe_to_perform() -> bool:
    with DBConnection() as connection:
        return connection.does_table_exist('user_account')


def migration() -> None:
    sql = """
        CREATE TABLE user_account (
            user_id INT PRIMARY KEY NOT NULL UNIQUE ,
            username TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """
    with DBConnection() as connection:
        connection.execute(sql)


if safe_to_perform():
    migration()

print(f'Successfull migration {basename(__file__)}')
