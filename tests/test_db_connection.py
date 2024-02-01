from database_handler.db_connection import DBConnection


def test_db_connection_builds_correct_insert_sql():
    DBConnection()._build_insert_sql('imaginary_table', [1, 2, 3, 4, 5])
