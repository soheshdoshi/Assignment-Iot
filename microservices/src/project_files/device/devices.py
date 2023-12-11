import datetime

from common_file import db_connection
from utils import utils
import logging

from typing import Any


class Device:
    def __init__(self):
        self.table_name = "device"
        self.db = db_connection.get_db()

    def check_device(self, name: str) -> bool:
        """
        this method will check device name available in db or not.
        """
        r = self.db.find_one(table=self.table_name, query={"deviceName": name})
        if r and len(r) > 0:
            return True
        return False

    def create_device(self, name: str, result_sensor_dict: dict) -> dict:
        """
        this method will create device with default sensor type.
        """
        device_dict = {
            "deviceName": name,
            "createAt": datetime.datetime.utcnow(),
            "ts": datetime.datetime.now().utcnow()
        }
        device_dict.update({
            "sensorData": result_sensor_dict
        })

        ack = self.db.insert(table=self.table_name, data=device_dict)
        logging.info(f"[INFO] :: {ack}")
        return ack

    def update_one_device_name(self, old_name: str, update_name: str) -> dict:
        """
        this method will use to update one record in db for device_name.
        """
        ack = self.db.update_one(table=self.table_name, query={"deviceName": old_name},
                                 update={"$set": {"deviceName": update_name}})

        logging.info(f"[INFO] :: {ack}")
        return ack

    def update_device_name(self, old_name: str, update_name: str) -> dict:
        """
        this method will use to update all record in db for device_name.
        """
        ack = self.db.update_many(table=self.table_name, query={"deviceName": old_name},
                                  update={"$set": {"deviceName": update_name}})
        logging.info(f"[INFO] :: {ack}")
        return ack

    def validate_new_device_name(self, device_name: Any) -> dict:
        """
        this method validate device name base on type and available in db.
        """
        if not utils.check_str(device_name):
            logging.info("[INFO] :: Invalid Key In Device Name.")
            return {"error": 400, "errorDescription": "Invalid key/device name."}
        if self.check_device(name=device_name):
            logging.info("[INFO] :: Device Name Exists.")
            return {"error": 409}
        return {}

    def validate_old_device_name(self, device_name: Any) -> dict:
        """
        this method validate device name base on type and available in db.
        """
        if not utils.check_str(device_name):
            logging.info("[INFO] :: Invalid Key In Device Name.")
            return {"error": 400, "errorDescription": "Invalid key/device name."}
        if not self.check_device(name=device_name):
            logging.info("[INFO] :: Device Name Exists.")
            return {"error": 409}
        return {}
