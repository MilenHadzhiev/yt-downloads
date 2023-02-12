import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import VideoEntry
from pytube import YouTube as yt
from flask_login import current_user, login_required
from validations import validate_personal_data, regex

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
            return render_template('profile_page.html')
        email = request.form.get('email')
        if not re.fullmatch(regex, email):
            flash('Email is incorrect format', category='error')
            return render_template('profile_page.html')
        user = User.query.filter_by(email=email).first()
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password1)
        db.session.commit()
        return redirect(url_for('views.profile'))
    user = current_user
    return render_template('profile_page.html', user=user)