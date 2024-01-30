from http import HTTPStatus
from typing import Optional

from backend.response.response import ResponseFactory, Response
from backend.response.response_data_mixin import ResponseDataMixin
from backend.setup import db
from flask import request
from flask_login import current_user

from backend.videos.video import Video
from backend.validations import validate_url


class VideoController(ResponseDataMixin):

    @staticmethod
    def __get_response_data(workflow: str, method: str, http_code: Optional[int] = 200, error: Optional[Exception] = None,
                            msg: Optional[str] = None) -> dict:
        return {
            'subject': 'Video',
            'action': workflow,
            'method': method,
            'http_code': http_code,
            'error': error,
            'msg': msg
        }

    def save_video(self) -> Response:
        # TODO if Configuration.database == 'sqllite':
        return self.__save_to_sql_lite()

    def edit(self) -> Response:
        video = Video.query.get(int(request.args.get('id')))
        data = self.__get_response_data('Edit video', 'VideoController.edit', HTTPStatus.OK)
        video.description = request.form.get('description') if request.form.get('description') else video.description
        video.has_been_downloaded = True if request.form.get('has_been_downloaded') else False
        db.session.commit()
        return ResponseFactory(data).success()

    def delete(self) -> Response:
        data = self.__get_response_data('Delete video', 'VideoController.delete')
        video_id = int(request.args.get('id'))
        video = Video.query.get(video_id)
        if video:
            if video.owner == current_user.id:
                db.session.delete(video)
                db.session.commit()
                data['http_code'] = HTTPStatus.OK
                return ResponseFactory(data).success()
            data['http_code'] = HTTPStatus.UNAUTHORIZED
            return ResponseFactory(data).error()
        data['http_code'] = HTTPStatus.NOT_FOUND
        return ResponseFactory(data).error()

    def __save_to_sql_lite(self) -> Response:
        url = request.form.get('url')
        data = self.__get_response_data('Save video to db', 'VideoController.__save_to_sql_lite')
        if not validate_url(url):
            data['http_code'] = HTTPStatus.BAD_REQUEST
            data['error'] = 'Invalid Youtube URL'
            data['msg'] = 'Please enter a valid Youtube URL'
            return ResponseFactory(data).error()
        video = Video.query.filter_by(url=url).first()
        if video:
            return ResponseFactory(data).already_exists()
        new_video = Video(
            url=url,
            description=request.form.get('description'),
            owner=current_user.id,
            has_been_downloaded=False
        )
        data['http_code'] = HTTPStatus.CREATED
        data['msg'] = 'success'
        db.session.add(new_video)
        db.session.commit()
        return ResponseFactory(data).success()
