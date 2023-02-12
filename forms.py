from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField

class VideoEditForm(FlaskForm):
    description = StringField('description')
    has_been_downloaded = BooleanField('has_been_downloaded')
