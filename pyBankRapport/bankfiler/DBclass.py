# Import required library
import os

from DButil import DButil
from bankfiler.logUtil import log
from configobj import ConfigObj

config = ConfigObj(os.getcwd() + '/config.ini')


def db_execution(start_post_rader):
    try:
        dbutil = DButil()
        connection = dbutil.__create_connection__()
        cursors = connection.cursor()
        if start_post_rader:

            for row in start_post_rader:
                queryq = "insert into temp_utbetfil (FILNAMN, RADNR, INFORMATION, P_ID,BELOPP,REGTS) values( " + row
                print(queryq)
                cursors.execute(queryq)
                rowcount = str(cursors.rowcount) + " " + "Rows Inserted"
                log.debug(rowcount)
        cursors.execute('commit')

    finally:
        pass


def db_insert_temp_filnamn(datem):
    dbutils = DButil()
    try:
        connection = dbutils.__create_connection__()
        cursors = connection.cursor()
        if datem:
            queryq = "insert into temp_filnamn (FILNAMN,REGTS) values( " + datem
            print(queryq)
            cursors.execute(queryq)
            rowcount = str(cursors.rowcount) + " " + "Rows Inserted"
            log.debug(rowcount)
            cursors.execute('commit')
    finally:
        cursors.close()
