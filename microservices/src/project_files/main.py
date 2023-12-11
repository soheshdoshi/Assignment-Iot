import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request, responses
from fastapi.encoders import jsonable_encoder

from common_file import error_handler
from router import status_router, device_router, sensor_router


# # pick logging.conf file for custom logger format
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
#
# logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def log_request(request: Request, call_next):
    """
    request middleware for format request and response.
    """
    idem = str(uuid4())
    logging.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        return responses.JSONResponse(
            status_code=500,
            content=jsonable_encoder(error_handler.get_statuscode(status_code=500)
                                     )
        )
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logging.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    return response


"""
Router Part for device & sensor route
"""
app.include_router(status_router.router)
app.include_router(device_router.router)
app.include_router(sensor_router.router)
