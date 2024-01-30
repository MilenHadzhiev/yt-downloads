import json
from http import HTTPStatus
from typing import Optional, Dict, Union


class Response:
    def __init__(self, message: str, response_code: int, additional_data: Optional[dict] = None):
        self.message = message
        self.response_code = response_code
        self.json = json.dumps(additional_data if additional_data else {})


class ResponseFactory:

    def __init__(self, data: Dict[str, Union[str, int]]):
        """"
        :param
            data is a dictionary with n keys:
            - subject: Model on which an operation was performed
            - action: Workflow from which the response orginates
            - method: The method which returns the Response
            - http_code: Optional
            - error: Optional - Detailed error description
            - msg: Optional - Additional information
        """
        self.__data = data

    @property
    def data(self) -> Dict[str, Union[str, int]]:
        return self.__data

    @classmethod
    def success(cls) -> Response:
        return Response('success', cls.data['http_code'] or HTTPStatus.OK)

    @classmethod
    def already_exists(cls) -> Response:
        return Response(f'{cls.data["subject"]} already exists', HTTPStatus.OK)

    @classmethod
    def _generic_error(cls, error: str, code: int, details: dict) -> Response:
        return Response(error, code, details)

    @classmethod
    def error(cls):
        return cls._generic_error(cls.data['error'], cls.data['http_code'], cls.data)

    @classmethod
    def programming_error(cls) -> Response:
        return cls._generic_error(
            'Internal Server Error',
            HTTPStatus.INTERNAL_SERVER_ERROR,
            {
                'error': cls.data['error'],
                'thrown_by': cls.data['method'],
                'during': cls.data['action']
            }
        )
