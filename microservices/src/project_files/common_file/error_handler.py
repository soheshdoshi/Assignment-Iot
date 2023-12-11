from fastapi import status
import logging

status_code_dict = {
    status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
    status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
    status.HTTP_402_PAYMENT_REQUIRED: "PAYMENT_REQUIRED",
    status.HTTP_403_FORBIDDEN: "FORBIDDEN",
    status.HTTP_404_NOT_FOUND: "RESOURCE_NOT_FOUND",
    status.HTTP_405_METHOD_NOT_ALLOWED: "METHOD_NOT_ALLOWED",
    status.HTTP_406_NOT_ACCEPTABLE: "NOT_ACCEPTABLE",
    status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED: "PROXY_AUTHENTICATION_REQUIRED",
    status.HTTP_408_REQUEST_TIMEOUT: "REQUEST_TIMEOUT",
    status.HTTP_409_CONFLICT: "CONFLICT",
    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: "UNSUPPORTED_MEDIA_TYPE",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "INTERNAL_SERVER_ERROR",
    status.HTTP_502_BAD_GATEWAY: "BAD_GATEWAY",
    status.HTTP_503_SERVICE_UNAVAILABLE: "SERVICE_UNAVAILABLE",
    status.HTTP_504_GATEWAY_TIMEOUT: "GATEWAY_TIMEOUT",
}


def get_statuscode(status_code: int, result=None, error_description=None) -> dict:
    """
    this custom statuscode method will return statuscode for endpoints.
    """
    if result is None:
        result = {}

    # this will handle error response
    if status_code >= 400:
        logging.info(f"[INFO] :: status_code :: {status_code}")
        return_dict = {"statusCode": status_code, "error": status_code_dict[status_code]}
        if error_description is not None:
            return_dict.update({
                "errorDescription": error_description
            })
        return return_dict

    # this will handle success response part.
    return {"statusCode": status_code, "result": result}
