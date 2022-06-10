#!/usr/bin/env python3
# -*- coding: utf-8 -*- L
# ----------------------------------------------------------------------------
# Created By  : Mickael Eriksson
# Created Date: 20220421
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Module to handle foreging payments in Återrapportering.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import time

"""
"""


class Cmd54dU:
    def __init__(self, processdate):
        super().__init__()
        self.processDate = processdate
        self.description = 'camt54Ud'
        self.rownum = 0
        self.filename = str(time.strftime('%y%m%d')) + "ut.ret"
        self.regts = "to_date('" + str(time.strftime('%Y-%m-%d')) + "','yyyy-mm-dd'))"

    def FirstPost(self):
        returnlist = list()
        rowdata = "'" + self.filename + "'," + str(self.rownum) + ",'xml version'," + self.regts
        returnlist.append(rowdata)
        self.rownum += 1
        rowdata1 = "'" + self.filename + "'," + str(
            self.rownum) + ",'" + "<dt>" + str(self.processDate) + "</dt>'," + self.regts  # Avipost
        self.rownum += 1
        returnlist.append(rowdata1)
        return returnlist

    def ParseForeginFile(self, rowdata):
        """

        :param rowdata:
        :param self:
        :return:
        """
        # <dt> pord datum
        # IFINSTR(l_information, '<Amt Ccy') > 0  AND INSTR(l_information, 'SEK') > 0 AND b_first = FALSE THEN
        #  IF INSTR(l_information,'<Ustrd>AVIID') > 0 AND b_traff = TRUE THEN
        returnlist = list()
        returnlist = self.FirstPost()
        for data in rowdata:
            rowdata = "'" + self.filename + "'," + str(self.rownum) + ",'" + '<Ustrd>'.rjust(29) + data[
                'avi'] + "</Ustrd>'," + self.regts  # Avipost
            self.rownum += 1
            rowdata1 = "'" + self.filename + "'," + str(self.rownum) + ",'" + '<Amt Ccy="'.rjust(33) + str(
                data['Ccy']) + ">" + str(data['amount']) + "</Amt>'," + self.regts  # Belopp
            self.rownum += 1
            returnlist.append( rowdata)
            returnlist.append( rowdata1)
        return returnlist
