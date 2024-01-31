from database_handler.DBConnection import DBConnection


def safe_to_perform() -> bool:
    pass


def migration():
    sql = """
        CREATE TABLE Video (
            video_id INT PRIMARY KEY NOT NULL UNIQUE,
            description VARCHAR(1500),
            url VARCHAR(255) NOT NULL,
            owner INT REFERENCES User(user_id),
            has_been_downloaded BOOLEAN DEFAULT FALSE,
        )
    """

    with DBConnection() as connection:
        connection.cursor().execute(sql)


if safe_to_perform():
    migration()
