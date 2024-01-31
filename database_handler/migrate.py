import os

from subprocess import call


def migrate() -> None:
    migrations = os.listdir("./migrations")
    migrations.remove('__init__.py')
    for migration in migrations:
        call(['python', migration])

migrate()