from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from setup import db


class User(db.Model, UserMixin):
    """
    Custom user model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(250))
    videos = db.relationship('VideoEntry')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password: str) -> str:
        return check_password_hash(self.password_hash, password)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __repr__(self) -> str:
        return self.__str__()


class VideoEntry(db.Model):
    """
    Store video entries in database
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    url = db.Column(db.String(250))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    has_been_downloaded = db.Column(db.Boolean)

    def __str__(self):
        return f'{self.url}'

    def __repr__(self):
        return f'{self.url}'
