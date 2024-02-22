from os.path import basename

from database_handler.db_connection import DBConnection


def safe_to_perform() -> bool:
    with DBConnection() as connection:
        return connection.does_table_exist('video')


def migration() -> None:
    sql = """
        CREATE TABLE video (
            video_id INT PRIMARY KEY NOT NULL UNIQUE,
            description VARCHAR(1500),
            url VARCHAR(255) NOT NULL,
            owner INT REFERENCES user_account(user_id),
            has_been_downloaded BOOLEAN DEFAULT FALSE
        )
    """

    with DBConnection() as connection:
        connection.execute(sql)


if safe_to_perform():
    migration()
print(f'Successfull migration {basename(__file__)}')
