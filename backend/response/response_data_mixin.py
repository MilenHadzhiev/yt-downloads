from typing import Optional


class ResponseDataMixin:
    @staticmethod
    def __get_response_data(workflow: str, method: str, http_code: Optional[int] = 200, error: Optional[Exception] = None,
                            msg: Optional[str] = None) -> dict:
        raise NotImplementedError
