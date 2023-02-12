from flask import Blueprint, render_template, request, redirect, url_for
from models import VideoEntry
from pytube import YouTube as yt

views = Blueprint('views', __name__)

@views.route('/')
def homepage():
    videos = VideoEntry.query.all()
    videos_data = [{
        'id': video.id,
        'desc': video.description,
        'title': yt(video.url).title,
        'url': video.url,
        'thumb': yt(video.url).thumbnail_url,
        'has_been_downloaded': video.has_been_downloaded
    } for video in videos]
    return render_template('homepage.html', videos=videos_data)
