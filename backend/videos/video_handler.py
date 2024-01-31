from backend.response.response import Response
from backend.videos.videos_controller import VideoController
from flask import Blueprint
from flask_login import login_required

video_api = Blueprint('video_api', __name__)
controller = VideoController()


@video_api.route('/add', methods=['GET', 'POST'])
def add_video() -> Response:
    return controller.save_video()


@video_api.route('/edit/', methods=['GET', 'POST'])
def edit() -> Response:
    return controller.edit()


@video_api.route('/download/', methods=['GET', 'POST'])
def download_video() -> Response:
    # TODO
    raise NotImplementedError


@video_api.route('/delete/')
@login_required
def delete_video() -> Response:
    return controller.delete()
