from os.path import exists
from typing import Union

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from views import views
from auth import auth
from videos import videos
from models import User

db = SQLAlchemy()
DB_NAME = 'yt-db.db'


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'zdr'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(videos, url_prefix='/video')

    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id: Union[int, str]):
        return User.query.get(int(user_id))
    return app


def create_database(app: Flask) -> None:
    if not exists(f'{DB_NAME}'):
        with app.app_context():
            db.create_all()
            print("Created database")
        return
    print('Database already exists')
