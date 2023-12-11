import json
import logging
import pymongo
import os
from threading import Lock

DB_ERROR = "db not initialized"
class MongoDb:
    def __init__(self, uri=None, db_name=None):
        self.connection = None
        self.db = None
        self.init_status = False
        self._reinit_lock = Lock()
        self.uri = uri
        self.db_name = db_name

    def start_init(self):
        """
        to start init create when server load.
        """
        return self.init()

    def init(self):
        """
        this will handle connection pool for db.
        """
        with self._reinit_lock:
            if self.init_status is True:
                try:
                    self.connection.server_info()
                except pymongo.errors.ServerSelectionTimeoutError:
                    self.init_status = False
                    logging.info("[INFO] :: [MongoDb] :: Reinitaing Connection!")
            if self.init_status is False:
                self.connection = pymongo.MongoClient(self.uri)
                self.db = self.connection[self.db_name]
                self.init_status = True
        return self

    @classmethod
    def from_config(cls, config_profile: str = "TEST", config_path: str = "config.json"):
        """
        this will load db config from config file
        """
        config = cls.__read_config(config_profile, config_path)
        if "URI" in config:
            uri = config["URI"]
            db_name = config["DB"]
            return cls(uri=uri, db_name=db_name)

    @staticmethod
    def __read_config(config_profile, config_path):
        """
        this method use for read config file for specific path.
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(dir_path, config_path)
        with open(config_path, "r") as f:
            config = json.loads(f.read())
        config_section = config[config_profile]
        return config_section

    def insert(self, table, data):
        """
        db insert method
        """
        if not self.init_status:
            raise AttributeError(DB_ERROR)

        if isinstance(data, list):
            t = self.db[table].insert_many(data)
            return_body = {
                "ack": t.acknowledged,
                "insertedIds": [t.inserted_ids]
            }
        elif isinstance(data, dict):
            t = self.db[table].insert_one(data)
            return_body = {
                "ack": t.acknowledged,
                "insertedIds": [t.inserted_id]
            }
        else:
            raise ValueError("MongoDb :: Invalid Value to insert, supported list, dict.")
        return return_body

    def update_one(self, table, query, update, *args, **kwargs):
        """
        this method use for update one record in db.
        """
        if not self.init_status:
            raise AttributeError(DB_ERROR)
        t = self.db[table].update_one(query, update, *args, **kwargs)
        return {
            'affectedRows': t.modified_count
        }

    def update_many(self, table, query, update, *args, **kwargs):
        """
        this method use for update multiple record in db.
        """
        if not self.init_status:
            raise AttributeError(DB_ERROR)
        t = self.db[table].update_many(query, update, *args, **kwargs)
        return {
            'affectedRows': t.modified_count
        }

    def remove(self, table, query):
        """
        this method use for delete record in db.
        """
        if not self.init_status:
            raise AttributeError(DB_ERROR)
        t = self.db[table].delete_many(query)
        return {
            'affectedRows': t.deleted_count
        }

    def find(self, table, query, projection=None):
        """
        this method use for find record in db.
        """
        if not self.init_status:
            raise AttributeError(DB_ERROR)
        return self.db[table].find(query, projection)

    def find_one(self, table, query, projection=None):
        """
        this method use for find one record in db.
        """
        if not self.init_status:
            raise AttributeError(DB_ERROR)
        return self.db[table].find_one(query, projection)

    def aggregate(self, table, query):
        """
        this method use for handle aggregate query.
        """
        if not self.init_status:
            raise AttributeError(DB_ERROR)
        return self.db[table].aggregate(query)

    def close_resources(self):
        """
        this method will close connection.
        """
        self.connection.close()
