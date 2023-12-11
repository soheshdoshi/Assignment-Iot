from .mongodb import MongoDb

global_db_conn = None

import logging


def get_db():
    """
    this method will use to reuse connection pool for db.
    """
    global global_db_conn
    if not global_db_conn:
        global_db_conn = MongoDb.from_config()
        logging.info("[INFO] :: Initializing New Db Connection")
        global_db_conn.init()
    return global_db_conn
