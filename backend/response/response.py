import json
from typing import Optional, Dict, Union


class Response:
    def __init__(self, message: str, response_code: int, additional_data: Optional[dict] = None):
        self.message = message
        self.response_code = response_code
        self.json = json.dumps(additional_data if additional_data else {})


class ResponseFactory:

    def __init__(self, data: Dict[str, Union[str, int]]):
        """"
        data is a dictionary with n keys:
            - subject: Model on which an operation was performed
            - action: Workflow from which the response orginates
            - method: The method which returns the Response
            - error: Detailed error description
            - msg: Additional information
        """
        self.__data = data

    @property
    def data(self) -> Dict[str, Union[str, int]]:
        return self.__data

    @classmethod
    def success(cls) -> Response:
        return Response('success', 200)

    @classmethod
    def already_exists(cls) -> Response:
        return Response(f'{cls.data["subject"]} already exists', 202)

    @classmethod
    def error(cls, error: str, code: int, details: dict) -> Response:
        return Response(error, code, details)

    @classmethod
    def programming_error(cls) -> Response:
        return cls.error('Internal Server Error', 500, {
            'error': cls.data['error'],
            'thrown_by': cls.data['method'],
            'during': cls.data['action']
        })
