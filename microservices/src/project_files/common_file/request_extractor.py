from abc import ABC

from fastapi import Request

from .error_handler import get_statuscode
from .jwt_token import auth_validation

import logging


class Extractor(ABC):
    """
    this class use for extract body parameter and return response.
    """

    def __init__(self, request_obj: Request):
        self.fast_api_obj: Request = request_obj
        self.path_parameters_dict: Request.path_params = request_obj.path_params
        self.headers: Request.headers = request_obj.headers
        self.request_method: Request.method = request_obj.method
        self.base_url: Request.base_url = request_obj.base_url
        self.client_id: Request.client = request_obj.client
        self.url: Request.url = request_obj.url
        self.json_body = None

    async def set_data(self):
        self.json_body = await self.fast_api_obj.json()
        logging.info("[INFO] :: json body data set.")

    def user_validation(self):
        """
        jwt user validation
        """
        _headers = self.headers.get("authorization", "")
        if len(_headers) <= 0:
            return {"error": 401}
        auth_response = auth_validation(_headers)
        if "error" in auth_response:
            return auth_response
        else:
            if auth_response["username"] != "sohesh":
                return {"error": 401}
        return auth_response

    def get_response(self, response: dict) -> dict:
        """
        this method will handle all response part.
        """
        if "error" in response:
            return get_statuscode(status_code=response["error"], result=None,
                                  error_description=response.get("errorDescription", ""))
        return get_statuscode(status_code=101, result=response)
