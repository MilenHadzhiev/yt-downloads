from backend.setup import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    thumbnail_url = db.column(db.String(250))
    description = db.Column(db.String(500))
    url = db.Column(db.String(250))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    has_been_downloaded = db.Column(db.Boolean)

    def __str__(self):
        return f'{self.url}'

    def __repr__(self):
        return f'{self.url}'
