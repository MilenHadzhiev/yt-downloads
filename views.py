import re

from pytube import YouTube as yt

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from models import VideoEntry, User
from validations import regex

from setup import db

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


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if request.form.get('password1') != request.form.get('password2'):
            flash('Passwords must match', category='error')
            return render_template('profile_page.html', user=current_user)
        user = User.query.get(int(current_user.id))
        email = request.form.get('email') if request.form.get('email') else user.email
        if not re.fullmatch(regex, email):
            flash('Email is incorrect format', category='error')
            return render_template('profile_page.html', user=current_user)
        user.username = request.form.get('username') if request.form.get('username') else user.username
        user.first_name = request.form.get('first_name') if request.form.get('first_name') else user.first_name
        user.last_name = request.form.get('last_name') if request.form.get('last_name') else user.last_name
        password1 = request.form.get('password1')
        if password1:
            user.set_password(password1)
        db.session.commit()
        return redirect(url_for('views.profile'))
    return render_template('profile_page.html', user=current_user)
