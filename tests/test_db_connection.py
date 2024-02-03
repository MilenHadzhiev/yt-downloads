from typing import Type

import pytest

from pytest_mock import MockerFixture

from database_handler.db_connection import DBConnection


def remove_whitespaces(string: str) -> str:
    return string.replace(' ', '').replace('\n', '').replace('\t', '')


def test_db_connection_builds_correct_insert_sql(mocker: MockerFixture):
    mocker.patch('psycopg2.connect')
    mocker.patch(
        'database_handler.db_connection.DBConnection._get_table_columns',
        return_value=['test_identity_column', 'test_column1', 'test_column2', 'time_stamp', 'user_stamp']
    )
    with DBConnection() as db:
        actual = db._build_insert_sql('test_table', [1, 'Alabala', 'test_value', '2023-01-03T12:34:56', 'mhadzhiev'])
        expected = "INSERT INTO test_table(test_identity_column, test_column1, test_column2, time_stamp, user_stamp) " \
                   "VALUES (1, 'Alabala', 'test_value', '2023-01-03T12:34:56', 'mhadzhiev');"

        assert remove_whitespaces(actual) == remove_whitespaces(expected)


@pytest.mark.parametrize('col_type',
                         (int, str),
                         ids=('Build sql for adding foreign key builds correct sql when fk is integer',
                         'Build sql for adding foreign key builds correct sql when fk is string'))
def test_db_connection_builds_correct_add_foreign_key_sql(mocker: MockerFixture, col_type: Type[str | int]):
    mocker.patch('psycopg2.connect')
    expected = f"""
    ALTER TABLE test_table
        ADD COLUMN student_id {'TEXT' if col_type is str else 'INT'}
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_student_id') THEN
        ALTER TABLE test_table
            ADD CONSTRAINT fk_student_id
            FOREIGN KEY (student_id) REFERENCES student(student_id);
    END IF;   
    """
    with DBConnection() as db:
        actual = db._build_add_foreign_key_sql('test_table', 'student', 'student_id', col_type)
        assert remove_whitespaces(actual) == remove_whitespaces(expected)
