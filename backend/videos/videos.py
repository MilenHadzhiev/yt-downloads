from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from backend.setup import db
from backend.videos.video import Video
from backend.validations import validate_url

from download import download
from forms import VideoEditForm
from typing import Type, Optional, Union
videos = Blueprint('videos', __name__)


def __add_video_to_db() -> Optional[Type["BaseResponse"]]:
    url = request.form.get('url')
    if not validate_url(url):
        flash('You must enter a youtube url', category='error')
        return render_template('add_video.html')
    video = Video.query.filter_by(url=url).first()
    if video:
        flash('Video already in queue', category='info')
        return redirect(url_for('views.homepage'))
    new_video = Video(
        url=url,
        description=request.form.get('description'),
        owner=current_user.id,
        has_been_downloaded=False
    )
    db.session.add(new_video)
    db.session.commit()
    if request.form.get('submit') == 'Save':
        return redirect(url_for('views.homepage'))
    else:
        flash('Video saved to queue', category='info')


@videos.route('/add', methods=['GET', 'POST'])
def add_video() -> str:
    if request.method == 'POST':
        __add_video_to_db()
    return render_template('add_video.html')


@videos.route('/edit/', methods=['GET', 'POST'])
def edit() -> Union[str, Type["BaseResponse"]]:
    video = Video.query.get(int(request.args.get('id')))
    print(request.form)
    if request.method == 'POST':
        video.description = request.form.get('description') if request.form.get('description') else video.description
        video.has_been_downloaded = True if request.form.get('has_been_downloaded') else False
        db.session.commit()
        return redirect(url_for('views.homepage'))
    return render_template('edit_video.html', form=VideoEditForm(), video=video)


@videos.route('/download/', methods=['GET', 'POST'])
def download_video() -> Type["BaseResponse"]:
    url = request.args.get('url')
    download(url)
    videos_with_given_url = Video.query.filter_by(url=url)
    for video in videos_with_given_url:
        video.has_been_downloaded = True
        db.session.commit()
    return redirect(url_for('views.homepage'))


@videos.route('/delete/')
@login_required
def delete_video() -> Type["BaseResponse"]:
    video_id = int(request.args.get('id'))
    video = Video.query.get(video_id)
    if video:
        if video.owner == current_user.id:
            db.session.delete(video)
            db.session.commit()
            flash('Video deleted from queue', category='info')
            return redirect(url_for('views.homepage'))
        flash('You don\'t own this queue so you can\'t delete videos from it', category='error')
    flash('Video not found', category='error')
    return redirect(url_for('views.homepage'))
