# ------------------------------------------------------------------------------
# Copyright (c) 2019, 2021, Oracle and/or its affiliates. All rights reserved.
#
# Portions Copyright 2007-2015, Anthony Tuininga. All rights reserved.
#
# Portions Copyright 2001-2007, Computronix (Canada) Ltd., Edmonton, Alberta,
# Canada. All rights reserved.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# bulk_aq.py
#   This script demonstrates how to use bulk enqueuing and dequeuing of
# messages with advanced queuing. It makes use of a RAW queue created in the
# sample setup.
#
# This script requires cx_Oracle 8.2 and higher.
# ------------------------------------------------------------------------------
import cx_Oracle
import cx_Oracle as oracleDb

from pyBankSkicka.BankSkicka.DButil import DButil
from pyBankSkicka.BankSkicka.NoEnvelope import NoEnvelope
from pyBankSkicka.BankSkicka.SecureEnvelope import SecureEnvelope


def output_type_handler(cursor, name, default_type, size, precision, scale):
    if default_type == cx_Oracle.DB_TYPE_CLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)
    if default_type == cx_Oracle.DB_TYPE_BLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG_RAW, arraysize=cursor.arraysize)


class QueueUtil:
    @staticmethod
    def getQueue():
        queue_name = "utbetfil_queue"
        # connect to database
        dbutil = DButil()
        connection = dbutil.__create_connection__()
        connection.outputtypehandler = output_type_handler
        # create queue
        utbet_type = connection.gettype("SPORT.UTBETFIL_TYPE")
        queue = connection.queue(queue_name, utbet_type)
        queue.deqoptions.wait = oracleDb.DEQ_WAIT_FOREVER
        queue.deqoptions.navigation = oracleDb.DEQ_FIRST_MSG
        queue.deqoptions.consumername = 'UTBET_SUBSCRIBER'
        # dequeue the messages
        print("\nDequeuing messages...")
        while True:
            for m in queue.deqMany(10):
                xml_file_name = m.payload.FILNAMN
                xml_str = m.payload.XMLFIL.read()
                if 'SCT' in xml_file_name:
                    SecureEnvelope.__secure_envelope__(xml_str)
                else:
                    NoEnvelope.__createXML__(xml_str)
                connection.commit()
