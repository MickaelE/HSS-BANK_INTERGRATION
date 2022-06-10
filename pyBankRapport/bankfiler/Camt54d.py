#!/usr/bin/env python3
# -*- coding: utf-8 -*- L
# ----------------------------------------------------------------------------
# Created By  : Mickael Eriksson
# Created Date: 20220421
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Module to convert from isofile to internal format.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import math
import os
import time
from collections import OrderedDict
from decimal import Decimal
from os.path import exists
from xml.etree.ElementTree import ParseError, parse

from configobj import ConfigObj
from dateutil import parser
from global_logger import Log
from numpy import double

import bankfiler.DBclass as dbClass
from bankfiler.Camt54dU import Cmd54dU
from bankfiler.Enums import BankGiroNum

log = Log.get_logger(logs_dir='logs')


def remove(string):
    """
    Strip file from whitespacec.
    Deprecated.
    param string: STring to strip
    :return: Stripped string.
    """
    return string.replace(" ", "")


def get_filename(path):
    """
    Get filname.
    :param path: Path inlusive filename.
    :return: Filename.
    """
    basename = os.path.basename(path)
    basename = basename[:12]
    return basename


def exsisting_rownr(ntrydtls):
    """
    Get a rownumber to use from instr.
    :param ntrydtls:
    :return: Rownummer
    """
    row_id = []
    ns = {'document': 'urn:iso:std:iso:20022:tech:xsd:camt.054.001.02'}
    for txdtls in ntrydtls:
        endtoendid = txdtls.find('.//document:Refs/document:EndToEndId', ns)
        if endtoendid is not None:
            row_cust_id = endtoendid.text.split('-')
            row_id.append(row_cust_id[1].zfill(10))
        else:
            log.info("no endtoendid")
    return row_id


def get_rownum(num, arr):
    """
    Get a rownumber to use.
    :param num: Number to use.
    :param arr:
    :return:
    """
    try:
        desired_array = [int(numeric_string) for numeric_string in arr]
        num = num + 1
        while num in desired_array:
            num += 1
        desired_array.append(num)
    except (Exception,):
        log.info("no get_rownum")
        num = 0
    finally:
        return num


def convert_int(number, decimals):
    """
    Converts a number and fill it to a string.
    :param number: Number to convert.
    :param decimals: How many decimals to convert to,
    :return: String representation of a decimal.
    """
    return str(number).zfill(decimals)


def getAccount(root, ns):
    """
    Find all bankgiros in the file.
    :param root: Xml root node.
    :param ns: String of xml schema.
    :return: List of bankgiros in the file.
    """
    account = list()
    deduplicated_list = list()
    txdtlses = root.findall(
        './/document:Ntry/document:NtryDtls/document:TxDtls', ns)
    for txdtls in txdtlses:
        if txdtls.find(
            './/document:RltdPties/document:DbtrAcct/document:Id/document'
            ':Othr/document:Id', ns) is not None:
            account.append(txdtls.find(
                './/document:RltdPties/document:DbtrAcct/document:Id'
                '/document:Othr'
                '/document:Id', ns).text)
    for item in account:
        if item not in deduplicated_list:
            deduplicated_list.append(item)
    return deduplicated_list


def is_number(s):
    """
    Check if a string is number only.
    Deprecated.
    :param s: String
    :return: True/False.
    """
    try:
        int(s)
        return True
    except ValueError:
        pass


def sumsup(ntrylist, bankgiro):
    ns = {'document': 'urn:iso:std:iso:20022:tech:xsd:camt.054.001.02'}
    partsum = 0
    for ntry in ntrylist:
        print('entry')
        bg = ntry.find(
            './/document:NtryDtls/document:TxDtls/RltdPties/document'
            ':DbtrAcct/document:Id/document:Othr'
            '/document:Id', ns)
        if bg is not None:
            print(bg.text)
            if bankgiro.contains(bg.text):
                partsum += ntry.find(',//document:Amt', ns).text

    return partsum


class InputsClass:
    """

    """

    @staticmethod
    def ParseDebitorFile(file_name: object) -> object:
        """

        :param file_name: Fil att hantera.
        :return:
        """

        ConfigObj(os.getcwd() + '/config.ini')
        # Parse XML with ElementTree
        log.info("Startar rapport: %s" % log.Levels.DEBUG)
        rad = 0
        start_post_id = "11"
        aviserings_post_id = "14"
        customer_id = "26"
        format_str = "%Y%m%d%H%M%S"
        timestr = str(time.strftime('%Y%m%d'))
        regts = "to_date('" + str(timestr) + "','yyyy-mm-dd')"
        existing = []
        data = []  # Data
        (amount, kundid) = ("''", "''")
        (russno, russsum) = (0, 0)
        (travno, travsum) = (0, 0)
        (utlno,utlsum) = (0,0)
        (totsumm, stackno) = (0,0)
        (errorno, errorsumtot, reftotno) = (0,0,0)
        (start_trav_post_rader, start_russ_post_rader) = (list(), list())
        cmd54du = Cmd54dU(timestr)  # Intiera utlandsbetningar.

        # Finns filen i verkligeten.
        if not exists(str(file_name)):
            log.info("No file exists with the name " + str(file_name))
            return
        try:
            tree = parse(file_name)
            root = tree.getroot()
            ns = {
                'document': 'urn:iso:std:iso:20022:tech:xsd:camt.054.001.02'
                            ''}  # namespace

            curr = root.find('.//document:Acct/document:Ccy', ns)  # Currency
            if curr:  # Går det att hämta valuta.
                curr = curr.text
            else:
                curr = ""
            bookgdate = root.find('.//document:CreDtTm', ns)  # Booking date.

            book = parser.parse(bookgdate.text)
            book_str = str(book.date().strftime("%y%m%d"))
            file_name_rad = "'" + book_str + 'bt.ret' + "'"
            temp_filnamn = "'bkstc" + str(book.date().strftime(
                format_str)) + "bt.ret'"  # Filnamn för tepm_filnman,
            table = "temp_utbetfil"
            account = getAccount(root, ns)
            ntrylist = root.findall('.//document:Ntry', ns)
            # ###############################################
            # Hantera bankgironummer och startpost 11.
            # Används endast för girobetalningar.
            # ###############################################
            for acc in account:
                if acc.startswith(str(BankGiroNum.russ.value)):  # Är det RUSS.
                    start_post = start_post_id + acc.rjust(10, '0') + \
                                 book_str.rjust(5) + "LEVERANTÖRSBETALNINGAR" \
                                 + book_str.rjust(5) + curr
                    start_russ_post_rader.append(
                        file_name_rad + ",'" + str(rad) + "','" + start_post +
                        "'," + kundid + "," + amount + "," + regts + ")")
                else:  # Stora hästtar.
                    start_post = start_post_id + acc.rjust(10, '0') + \
                                 book_str.rjust(5) + "LEVERANTÖRSBETALNINGAR" \
                                 + book_str.rjust(5) + curr
                    start_trav_post_rader.append(
                        file_name_rad + ",'" + str(rad) + "','" + remove(
                            start_post) + "'," + kundid + "," + amount +
                        "," + regts + ")")
            # Registrigngs datum, som används i alla rader.
            regts = "to_date('" + str(book.date()) + "','yyyy-mm-dd')"  #
            # #######################################################################
            # Entries är det som delar mellan utlänskt och giro.
            # #######################################################################
            for Ntry in ntrylist:
                # NtryDtls
                txdtlslist = Ntry.findall('.//document:NtryDtls/document'
                                          ':TxDtls', ns)
                existing = exsisting_rownr(txdtlslist)
                # Detaleljer
                for txdtls in txdtlslist:
                    log.debug('startar txtdtls')
                    instrid = txdtls.find('.//document:Refs/document:InstrId',
                                          ns)
                    avinr = txdtls.find('.//document:RmtInf/document:Ustrd',
                                        ns)
                    bg = txdtls.find('.//document:RltdPties/document'
                                     ':DbtrAcct/document:Id/document:Othr'
                                     '/document:Id',
                                     ns)  # Trav, russ eller galopp? bg.....
                    if bg is not None:  # Finns det något bankgiro?
                        bg = bg.text
                        log.debug('Bankgiro: ' + bg)
                    # ##########################################################
                    # Giro betalningar.
                    # ##########################################################
                    if instrid is not None and not \
                        avinr.text.isdigit() is False:
                        # För var bankgiro, hantera radnr och kö.
                        log.debug('instrid: ' + instrid.text)
                        if '-' in instrid.text:  # Om det finns ett
                            # texten, splitta i beståndsdelar.
                            pmtinfid = instrid.text.split('-')
                            log.debug('pmtinfid ' + str(len(pmtinfid)))
                            row_cust_id = txdtls.find(
                                './/document:Refs/document:EndToEndId', ns)
                            log.debug(row_cust_id)
                            if row_cust_id is not None:  # Fick vi tag i
                                # kundnummer?
                                row_cust_id = row_cust_id.text.split('-')
                                row_id = row_cust_id[1].zfill(10)
                                kundid = row_cust_id[0].zfill(9)
                            else:
                                rad += 1
                                row_id = str(get_rownum(rad, existing))
                            if not is_number(kundid):
                                kundid = ''

                            existing.append(row_id)
                            utbetalningsnr = txdtls.find(
                                './/document:CdtrAcct/document:Id/document'
                                ':Othr/document:Id',
                                ns)  # OCR nummer.
                            if utbetalningsnr is not None:
                                utbetalningsnr = utbetalningsnr.text[0: 8]
                                utbetalningsnr = utbetalningsnr.zfill(9)
                            else:
                                utbetalningsnr = '1'
                            if not is_number(utbetalningsnr):
                                utbetalningsnr = ''
                            amt = txdtls.find(
                                './/document:AmtDtls/document:TxAmt/document'
                                ':Amt',
                                ns)

                            amount_ore = math.trunc(Decimal(amt.text) * 100)
                            # ###############################################
                            # Aviseringspost(14): Utbetalningsnr Kundnr
                            # Avinr Belopp i ören Bokföringsdatum
                            # ###############################################
                            utbetalningsnr = utbetalningsnr.zfill(9)
                            fill = 22 - len(aviserings_post_id)
                            avi = avinr.text.replace('-', '').zfill(16)
                            avi1 = avi.zfill(fill + 15 - len(utbetalningsnr))
                            amount_ore_len = str(amount_ore).zfill(12)

                            bet = aviserings_post_id + utbetalningsnr + avi1\
                                  + \
                                  amount_ore_len
                            rad += 1
                            rad = get_rownum(rad, existing)
                            aviserings_rad = file_name_rad + ",'" + str(
                                rad) + "','" + bet + "'" + ",'" + kundid + \
                                             "'," + str(
                                amount_ore) + "," + regts + ")"
                            if aviserings_rad is not None:
                                if bg.startswith(BankGiroNum.russ.value):
                                    start_russ_post_rader.append(
                                        aviserings_rad)
                                    russsum += amount_ore
                                    russno += 1
                                else:

                                    travno += 1
                                    travsum += amount_ore
                                    start_trav_post_rader.append(
                                        aviserings_rad)
                            # ###############################################
                            #  Kontonummerpost(26)
                            # ###############################################
                            cdtracct = txdtls.find('.//document:CdtrAcct', ns)
                            cred_name = txdtls.find(
                                './/document:Cdtr/document:Nm', ns)
                            if cdtracct is not None:  # Nordea seems to not
                                # use this often.
                                # cdrid = txdtls.find(
                                # './/document:CdtrAcct/document:Id', ns)
                                if cred_name is not None:
                                    creditor = "q'[" + customer_id + row_id \
                                               + " " + cred_name.text + "]'"
                                else:
                                    creditor = "q'[" + customer_id + \
                                               row_id.zfill(
                                                   10) + " Manuell]'"
                                log.debug('startar rader')
                                # Kund 26 Löpnr, Namn ev CO-adress
                                rad += 1
                                rad = get_rownum(rad, existing)
                                kund_rad = file_name_rad + ",'" + str(
                                    rad) + "'," + creditor + ",'" + kundid + \
                                           "'," + amount + "," + regts + ") "
                                if kund_rad is not None and \
                                    bg.startswith(BankGiroNum.russ.value):
                                    start_trav_post_rader.append(kund_rad)
                                else:
                                    log.debug("no kundrad")
                            else:
                                # ###############################################
                                #  Adresspost(27)
                                # ###############################################
                                avipost = '[27' + str(rad).rjust(10,
                                                                 '0') + \
                                          cred_name.text + ']'
                                rad += 1
                                rad = get_rownum(rad, existing)
                                avi_rad = file_name_rad + "," + str(
                                    rad) + ",q'" + avipost + "'," + amount + \
                                          ",''," + regts + ") "
                                if avi_rad is not None:
                                    if bg.startswith(BankGiroNum.russ.value):
                                        start_russ_post_rader.append(avi_rad)
                                    else:
                                        start_trav_post_rader.append(avi_rad)

                    else:
                        # #########################################################
                        # Utlandsbetalingar hanteras in en separat file
                        # *****ut.ret
                        # #########################################################
                        utlamount = txdtls.find(
                            './/document:AmtDtls/document:TxAmt/document:Amt',
                            ns)
                        ccy = utlamount.attrib['Ccy']
                        utlno += 1
                        utlsum += double(utlamount.text)
                        row = {'datum': book_str, 'avi': avinr.text,
                               'amount': utlamount.text, 'Ccy': ccy}

                        data.append(row)

                        # End tkx
                # ###############################################
                # post 29  Ej nödvändig för utlandsbetalingar.
                # ################################################
            for acc in account:
                if acc.startswith(BankGiroNum.russ.value):
                    summpost = '29' + acc.zfill(10) + str(russno).zfill(
                        8) + str(russsum).rjust(
                        12, '0')
                    rad = get_rownum(rad, existing)
                    start_russ_post_rader.append(
                        file_name_rad + ",'" + str(rad) + "','" + remove(
                            summpost) + "',"
                        + kundid + "," + amount + "," + regts + ")")
                else:
                    summpost = '29' + acc.rjust(10, '0') + \
                               str(travno).rjust(8, '0') + str(
                        travsum).rjust(
                        12, '0')
                    rad = get_rownum(rad, existing)
                    start_trav_post_rader.append(
                        file_name_rad + ",'" + str(rad) + "','" + remove(
                            summpost) + "',"
                        + kundid + "," + amount + "," + regts + ")")
                existing.append(rad)
            # Stänger utl fil.
            start_utl_post_rader = cmd54du.ParseForeginFile(data)

            # ###############################################
            # Databas relaterat.
            # ###############################################
            travsum = travsum / 100
            utlsum = utlsum / 100
            russsum = russsum / 100
            reftot = (utlsum + russsum + travsum + errorsumtot)  # Totalsum
            delta = totsumm - reftot  # Delta mellan beräknad och xml värde
            log.debug('startar rader')
            log.info("#######################################################")
            log.info("Summering av körning")
            log.info('Antal travposter ' + str(travno) + ' Varav ' +
                     str(errorno) + ' är fel och summa ' + str(
                travsum) + ' SEK varav ' + str(errorsumtot) +
                     ' SEK är Fel')
            log.info('Antal russposter ' + str(russno) + ' och summa ' + str(
                russsum) + ' SEK')
            log.info(
                'Antal utlposter ' + str(utlno) + ' och summa ' + str(
                    utlsum) + ' SEK')
            log.info(
                'Antal totalt ' + str(reftotno) + ' och summa ' + str(
                    round(reftot, 2)) +
                ' antal Stacks: ' + str(stackno) + ' Delta ' +
                str(round(delta, 2)) + ' SEK')
            log.info("#######################################################")
            if start_utl_post_rader is not None:
                dbClass.remove_temp_utbetfil("'" + cmd54du.filename + "'",
                                             table_name=table, no=1)
                dbClass.db_execution(start_post_rader=start_utl_post_rader,
                                     table_name=table, no=1)
                log.debug(
                    '########################################################')
            if start_trav_post_rader is not None:
                rader = list(OrderedDict.fromkeys(start_trav_post_rader))
                regist_fil = temp_filnamn + "," + regts + ")"
                dbClass.remove_temp_filesname(temp_filnamn, no=1)
                dbClass.remove_temp_utbetfil(file_name_rad, table_name=table,
                                             no=1)
                dbClass.db_insert_temp_filnamn(datem=regist_fil, no=1)
                dbClass.db_execution(start_post_rader=rader, table_name=table,
                                     no=1)
                log.debug(
                    '########################################################')
            if start_russ_post_rader is not None:
                rader = list(OrderedDict.fromkeys(start_russ_post_rader))
                regist_fil = temp_filnamn + "," + regts + ")"
                dbClass.remove_temp_filesname(temp_filnamn, no=2)
                dbClass.remove_temp_utbetfil(file_name_rad, table_name=table,
                                             no=2)
                dbClass.db_insert_temp_filnamn(datem=regist_fil, no=2)
                dbClass.db_execution(start_post_rader=rader, table_name=table,
                                     no=2)
        except ValueError as e:
            log.error("ParseDebitorFile Error: " + str(e))
            raise ValueError("ParseDebitorFile Error: " + str(e))
        except ParseError as err:
            log.error('ParseDebitorFile Error: ' + str(err))
        except (
            FileNotFoundError, TypeError, RuntimeError, KeyError, NameError,
            IOError, NotImplementedError,
            SyntaxError) as err:
            log.error('ParseDebitorFile Error: ' + str(err))
        except Exception as err:
            log.error("ParseDebitorFile Error: " + str(err))
        finally:
            log.info('ParseDebitorFile info: cam54bt done')
            return 0

    @classmethod
    def Inparsecam54(cls, xmlfile):
        pass
