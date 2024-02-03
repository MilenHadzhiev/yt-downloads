from os.path import basename

from database_handler.db_connection import DBConnection


def safe_to_perform() -> bool:
    sql = """
        SELECT NOT EXISTS (
            SELECT FROM 
                pg_tables
            WHERE 
                schemaname = 'public' AND 
                tablename  = 'video'
    )
    """

    with DBConnection() as connection:
        return connection.get_raw_response(sql)[0][0]


def migration():
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
