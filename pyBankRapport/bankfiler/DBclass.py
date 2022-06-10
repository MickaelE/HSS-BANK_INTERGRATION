#!/usr/bin/env python3
# -*- coding: utf-8 -*- L
# ----------------------------------------------------------------------------
# Created By  : Mickael Eriksson
# Created Date: 20220421
# version ='1.0'
# ---------------------------------------------------------------------------
"""
This module is for handling database calls. The reason beeing to make a central
place for database calls.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import os

import cx_Oracle
from configobj import ConfigObj
from global_logger import Log

from bankfiler.DButil import DButil

log = Log.get_logger(logs_dir='logs')
config = ConfigObj(os.getcwd() + '/config.ini')
global cursors


def db_execution(start_post_rader, table_name: str, no=1):
    """
    Kör sql i databasen för temp_filnamn.
    :param start_post_rader: En lista med sql rader.
    :param table_name: Vilken tabell.
    :param no: Aanvänds inte
    :return: status.
    """
    global cursors
    try:
        dbutil = DButil()
        queryq = None
        if start_post_rader:
            connection = dbutil.__create_connection__(no)
            cursors = connection.cursor()
            for row in start_post_rader:
                if table_name == 'temp_utbetfil' and 'bt.ret' in row:
                    queryq = "insert into temp_utbetfil (FILNAMN, RADNR, " \
                             "INFORMATION, P_ID,BELOPP,REGTS) values( " + row
                elif 'ut.ret' in row:
                    queryq = "insert into temp_utbetfil (FILNAMN, RADNR, " \
                             "INFORMATION,REGTS) values( " + row
                elif 'bt.bi' in row:
                    queryq = "insert into temp_inbetfil (FILNAMN, RADNR," \
                             "POSTTYP, INFORMATION, O_KOD, REGTS) values( " \
                             + row
                log.info(queryq)
                cursors.execute(queryq)
                rowcount = str(cursors.rowcount) + " " + "Rows Inserted"
                log.debug(rowcount)
            connection.commit()
    except Exception as es:
        log.error('db_execution: ' + str(es))
    finally:
        cursors.close()


def db_insert_temp_filnamn(datem, no=1):
    """
    Lägger till en rad för filen itemp_filnamn
    :param datem: Filnamn.
    :param no: Används inte.
    :return: Resultat.
    """
    global cursors
    dbutils = DButil()
    try:
        connection = dbutils.__create_connection__(no)
        cursors = connection.cursor()
        if datem:
            queryq = "insert into temp_filnamn (FILNAMN,REGTS) values( " + \
                     datem
            log.info(queryq)
            cursors.execute(queryq)
            rowcount = str(cursors.rowcount) + " " + "Rows Inserted"
            log.debug(rowcount)
        connection.commit()
    except Exception as es:
        log.error('db_insert_temp_filnamn: ' + str(es))
    finally:
        cursors.close()


def remove_temp_filesname(filename, no=1):
    """
    Tar bort filposten (om den finns).
    :param filename: Filnamnet som ska tas bort.
    :param no: Används inte,
    :return:  Resultat.
    """
    global cursors
    dbutils = DButil()
    try:
        connection = dbutils.__create_connection__(no)
        cursors = connection.cursor()
        if filename:
            queryq = "delete from temp_filnamn where FILNAMN = " + filename
            log.info(queryq)
            cursors.execute(queryq)
            rowcount = str(cursors.rowcount) + " " + "Rows Deleted"
            log.debug(rowcount)
        connection.commit()
    except Exception as es:
        log.error('remove_temp_filesname: ' + str(es))
    finally:
        cursors.close()


def remove_temp_utbetfil(filename, table_name: str, no=1):
    """
    Tar bort rader som tillhör ett filnamn (om de finns).
    :param filename: Namnet på filen vars rader ska raderas.
    :param table_name:  Tabell namn.
    :param no: Används inte.
    :return: Resultat.
    """
    global cursors
    dbutils = DButil()
    try:
        connection = dbutils.__create_connection__(no)
        cursors = connection.cursor()
        if filename:
            queryq = "delete from " + table_name + " where FILNAMN =" + \
                     filename
            log.info(queryq)
            cursors.execute(queryq)
            rowcount = str(cursors.rowcount) + " " + "Rows Delete"
            log.debug(rowcount)
        connection.commit()
    except Exception as es:
        log.error('remove_temp_utbetfil: ' + str(es))
    finally:
        cursors.close()


def kresklogg_rec_object(con, value):
    record_type = con.gettype('SPORT.KSP_KRESKLOGGNING.KRESKLOGG_REC')
    rec = record_type.newobject()
    rec.PROC_KOD = value['proc_kod']
    rec.O_KOD = value['o_kod']
    rec.JOUR_NR = int(value['jour_nr'])
    rec.PROCNAMN = value['procnamn']
    rec.TEXT = value['text']
    rec.FELTYP = value['feltyp']
    rec.ERRORCODE = value['errorcode']
    rec.ERRORMESSAGE = value['errormessage']
    return rec


def CallProcedure(procname, procparameters, no=1):
    dbutils = DButil()
    cursor = None
    try:
        connection = dbutils.__create_connection__(no)
        cursor = connection.cursor()
        cursor.callproc("dbms_output.enable")
        obj = kresklogg_rec_object(connection, procparameters)
        cursor.callproc(procname,[obj])
    except cx_Oracle.Error as es:
        log.error('remove_temp_utbetfil: ' + str(es))
    except cx_Oracle.Warning as oe:
        log.error('remove_temp_utbetfil: ' + str(oe))
    finally:
        pass
        # cursor.close()
