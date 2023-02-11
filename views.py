from flask import Blueprint, render_template
from models import VideoEntry
views = Blueprint('views', __name__)

@views.route('/')
def homepage():
    videos = VideoEntry.query.all()
    return render_template('homepage.html', videos=videos)

def add_video():
    pass