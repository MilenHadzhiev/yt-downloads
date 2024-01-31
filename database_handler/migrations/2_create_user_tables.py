from database_handler.DBConnection import DBConnection

def safe_to_perform() -> bool:
    pass


def migration():
    sql = """
        CREATE TABLE User (
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