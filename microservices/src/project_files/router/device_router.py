import json

from bson import json_util
from fastapi import APIRouter, Request

from common_file import request_extractor
from device import devices
from sensor import sensor

router = APIRouter()
device_obj = devices.Device()
sensor_obj = sensor.Sensor()


@router.post("/shoreline/devices")
async def device_router(request: Request):
    """
    this function will handle all post request for device creation part.
    """

    # request body extraction part
    extractor_obj = request_extractor.Extractor(request_obj=request)
    await extractor_obj.set_data()

    # jwt part
    validation_response = extractor_obj.user_validation()
    if "error" in validation_response:
        return extractor_obj.get_response(response=validation_response)

    # request body validation part.
    request_body = extractor_obj.json_body
    validation_res = device_obj.validate_new_device_name(request_body.get("device_name", None))
    if "error" in validation_res:
        return extractor_obj.get_response(response=validation_res)

    result_sensor_dict = {}
    for key in sensor_obj.get_sensor_type({}):
        result_sensor_dict.update({
            key: sensor.SENSOR_ENUM[key]
        })

    # after validation call create device for db part.
    result_response = device_obj.create_device(request_body["device_name"], result_sensor_dict=result_sensor_dict)

    # we have mongodb obj in response for serialization we use this
    result_response = json.loads(json_util.dumps(result_response))

    # return custom response
    return extractor_obj.get_response(response=result_response)


@router.patch("/shoreline/devices")
async def update_device_router(request: Request):
    """
    this method will use for update device name for one record in db.
    """

    # request body extraction part
    extractor_obj = request_extractor.Extractor(request_obj=request)
    await extractor_obj.set_data()
    request_body = extractor_obj.json_body

    # request body validation part.
    old_validation_res = device_obj.validate_old_device_name(request_body.get("old_device_name", None))
    if "error" in old_validation_res:
        return extractor_obj.get_response(response=old_validation_res)
    new_name_validation = device_obj.validate_new_device_name(request_body.get("new_device_name", None))
    if "error" in old_validation_res:
        return extractor_obj.get_response(response=new_name_validation)

    # after validation call update device for db part.
    result_response = device_obj.update_one_device_name(old_name=request_body["old_device_name"],
                                                        update_name=request_body["new_device_name"])

    # return custom response
    return extractor_obj.get_response(response=result_response)


@router.put("/shoreline/devices")
async def update_device_router(request: Request):
    """
    this method will update all record for device name
    """

    # request body extraction part
    extractor_obj = request_extractor.Extractor(request_obj=request)
    await extractor_obj.set_data()
    request_body = extractor_obj.json_body

    # request body validation part.
    old_validation_res = device_obj.validate_old_device_name(request_body.get("old_device_name", None))
    if "error" in old_validation_res:
        return extractor_obj.get_response(response=old_validation_res)
    new_name_validation = device_obj.validate_new_device_name(request_body.get("new_device_name", None))
    if "error" in old_validation_res:
        return extractor_obj.get_response(response=new_name_validation)

    # after validation call update device for db part.
    result_response = device_obj.update_device_name(old_name=request_body["old_device_name"],
                                                    update_name=request_body["new_device_name"])

    # return custom response
    return extractor_obj.get_response(response=result_response)
