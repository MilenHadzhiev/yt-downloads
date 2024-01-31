import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        database=os.environ.get('db_name', 'yt_downloads'),
        user=os.environ.get('user', 'postgres'),
        password=os.environ.get('pass', 'postgres'),
        host=os.environ.get("host", "localhost"),
        port=os.environ.get("port", 5432)
    )


def main() -> None:
    db_connection = get_connection()
    cursor = db_connection.cursor()
    print(cursor.execute("select * from yt_downloads"))

if __name__ == '__main__':
    main()
