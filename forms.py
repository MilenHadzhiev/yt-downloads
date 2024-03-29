from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField


class VideoEditForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """
    Reuse basic Flask Form to edit video
    """
    description = StringField('description')
    has_been_downloaded = BooleanField('has_been_downloaded')
