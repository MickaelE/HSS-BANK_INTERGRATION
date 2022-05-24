#  Copyright (c) 2022. Mickael Eriksson

import os
import cx_Oracle
from configobj import ConfigObj, ConfigObjError, ConfigspecError
from global_logger import Log

"""
"""

log = Log.get_logger(logs_dir='logs')


class DButil:

    def __init__(self):
        self.config = ConfigObj(os.getcwd() + '/config.ini')
        self.dsn = cx_Oracle.makedsn(host=self.config['db']["host"], port=self.config['db']["port"],
                                     service_name=self.config['db']["service_name"])

    def __create_pool__(self):
        """
        Create a connection pool for oracle
        :return: pool connections
        """
        # Create the session pool
        log.debug("Creating pool")
        try:
            pool = cx_Oracle.SessionPool(user=self.config['db']["user"], password=self.config['db']["passwd"],
                                         dsn=self.dsn, min=2, threaded=True, events=True,
                                         max=5, increment=1, encoding="UTF-8")
        except cx_Oracle.error:
            log.error("Error creating pool")
        return pool

    def __create_connection__(self):
        """
        Create a connection to a Oracle database.
        :return: Oracle connection.
        """
        print(self.dsn)
        return cx_Oracle.connect(user=self.config['db']["user"], password=self.config['db']["passwd"], dsn=self.dsn)
