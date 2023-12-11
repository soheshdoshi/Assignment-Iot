import json
from datetime import datetime

from fastapi import APIRouter, Request
from common_file import request_extractor
from device import devices
from sensor import sensor
from utils import utils
from bson import json_util

from collections import defaultdict

router = APIRouter()
sensor_obj = sensor.Sensor()
device_obj = devices.Device()


@router.post("/shoreline/sensors")
async def device_router(request: Request):
    """
    this method will add sensor value in db base on device_name
    """

    # request body extraction part
    extractor_obj = request_extractor.Extractor(request_obj=request)
    await extractor_obj.set_data()
    request_body = extractor_obj.json_body

    # extract all request body param
    device_name = request_body.get("device_name", None)
    sensor_type = request_body.get("sensor_type", None)
    value = request_body.get("value", None)

    # validation on param
    if device_name is None or sensor_type is None or value is None:
        return extractor_obj.get_response(response={
            "error": 400,
            "errorDescription": "Invalid key"
        })

    if isinstance(value, int) or isinstance(value, float):
        value = float(value)

    device_validation = device_obj.validate_old_device_name(device_name=device_name)
    if "error" in device_validation:
        return extractor_obj.get_response(response=device_validation)

    sensor_validation = sensor_obj.validate_sensor_type(sensor_type=sensor_type)
    if "error" in sensor_validation:
        return extractor_obj.get_response(response=sensor_validation)

    value_validation = utils.check_value(value=value)

    if not value_validation:
        return extractor_obj.get_response(response={"error": 400, "errorDescription": "Invalid sensor value."})

    # call db op for insert data
    result_response = sensor_obj.send_data_to_sensor(
        device_name=request_body["device_name"],
        sensor_type=request_body["sensor_type"],
        value=request_body["value"]
    )

    # we have mongodb obj in response for serialization we use this
    result_response = json.loads(json_util.dumps(result_response))

    # return custom response
    return extractor_obj.get_response(response=result_response)


@router.get("/shoreline/sensors")
async def get_sensor_data_base_on_device(request: Request):
    """
    this method will return sensor data base-on device and sensor type.
    """
    result_dict = defaultdict(list)

    # request body extraction part
    extractor_obj = request_extractor.Extractor(request_obj=request)
    await extractor_obj.set_data()
    request_body = extractor_obj.json_body

    device_name = request_body.get("device_name", None)

    # request body validation part.
    device_validation = device_obj.validate_old_device_name(device_name=device_name)
    if "error" in device_validation:
        return extractor_obj.get_response(response=device_validation)

    sensor_type = request_body.get("sensor_type", None)
    if sensor_type not in sensor.SENSOR_ENUM.keys():
        return extractor_obj.get_response(response={
            "error": 400,
            "errorDescription": "Invalid sensor type"
        })

    start_time = request_body.get("start_time", "")
    end_time = request_body.get("end_time", "")

    try:
        # str to time obj conversion for mongodb
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
    except Exception:
        return extractor_obj.get_response(response={
            "error": 400,
            "errorDescription": "Invalid Date Range :: hint %Y-%m-%dT%H:%M:%S"
        })

    # call db op for get all sensor data after validation
    result_cursor = sensor_obj.get_sensor_data_base_on_device_name(device_name=device_name,
                                                                   sensor_type=sensor_type,
                                                                   start_time=start_time,
                                                                   end_time=end_time)

    # create response dict
    for result in result_cursor:
        if sensor_type in result.get("sensorData", {}):
            result_dict[sensor_type].append(result["sensorData"][sensor_type])

    # return custom response
    return extractor_obj.get_response(response=result_dict)
