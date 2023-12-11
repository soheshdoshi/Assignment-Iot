import datetime
import logging
from collections import defaultdict

from common_file import db_connection
from utils import utils, convertor

from typing import DefaultDict, Dict, Any

SENSOR_ENUM = {
    "pressure": 0,
    "temperature": {
        "fahrenheit": 0,
        "celsius": 0
    }
}


class Sensor:
    def __init__(self):
        self.table_name: str = "sensors"
        self.sensor_dict: DefaultDict = defaultdict(dict)
        self.db = db_connection.get_db()  # mongodb connection obj

    def check_sensor_type(self, sensor_type: str) -> bool:
        """
        this method will check sensor_type is available in db or not.
        """
        r = self.db.find_one(table=self.table_name, query={"type": sensor_type})
        if r and len(r) > 0:
            return True
        return False

    def get_sensor_type(self, query=None) -> DefaultDict:
        """
        this method will return all sensor type in db.
        """
        if query is None:
            query = {}
        cursor = self.db.find(table=self.table_name, query=query)
        for record in cursor:
            self.sensor_dict[record['type']] = str(record['_id'])
        return self.sensor_dict

    def send_data_to_sensor(self, sensor_type: str, device_name: str, value: float) -> Dict:
        """
        this method will insert sensor data in db base on device_name and sensor_type.
        """
        result_dict = {
            "deviceName": device_name,
            "ts": datetime.datetime.utcnow(),
        }

        sensor_data_dict = {
            "sensorData": {
            }
        }
        if sensor_type == "temperature":
            # conversion part for temperature celsius_to_fahrenheit
            fahrenheit_value = convertor.celsius_to_fahrenheit(value)
            sensor_data_dict["sensorData"].update({
                sensor_type: {
                    "fahrenheit": fahrenheit_value,
                    "celsius": value
                }
            })
        else:
            # no conversion required for other type.
            sensor_data_dict["sensorData"].update({
                sensor_type: value
            })
        result_dict.update({
            "sensorData": sensor_data_dict["sensorData"]
        })
        ack = self.db.insert(table="device", data=result_dict)
        logging.info(f"[INFO] :: {ack}")
        return ack

    def validate_sensor_type(self, sensor_type: Any) -> Dict:
        """
        this method will check sensor_type is str or not also check sensor_type is available in db or not.
        """
        if not utils.check_str(sensor_type):
            return {"error": 400, "errorDescription": "Invalid key/sensor type."}
        if not self.check_sensor_type(sensor_type=sensor_type):
            return {"error": 409}
        return {}

    def get_sensor_data_base_on_device_name(self, device_name: str, sensor_type: str,
                                            start_time: datetime, end_time: datetime):
        """
        this method will return sensor value base on device_name, sensor_tye and date range.
        """

        cursor = self.db.find(table="device",
                              query={
                                  "deviceName": device_name,
                                  "ts": {
                                      "$gte": start_time,
                                      "$lte": end_time
                                  }
                              },
                              projection={
                                  f"sensorData.{sensor_type}": 1,
                                  "_id": 0
                              })
        return cursor
