#!/usr/bin/env python3
# -*- coding: utf-8 -*- L
# ----------------------------------------------------------------------------
# Created By  : Mickael Eriksson
# Created Date: 20220421
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Module to convert from isofile to bgMAx format.
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
from tokenize import String
from xml.etree.ElementTree import parse, ParseError
from configobj import ConfigObj
from dateutil import parser
from global_logger import Log
import bankfiler.DBclass as dbClass
from bankfiler.Enums import BankGiroNum

log = Log.get_logger(logs_dir='logs')


def remove(string):
    return string.replace(" ", "")


def getAccount(root, ns):
    """
    Find all bankgiros in the file.
    :param root: Xml root node.
    :param ns: String of xml schema.
    :return: List of bankgiros in the file.
    """
    account = list()
    deduplicated_list = list()
    txdtlses = root.findall('.//document:Ntry/document:NtryDtls/document'
                            ':TxDtls', ns)
    #
    for txdtls in txdtlses:
        if txdtls.find('.//document:RltdPties/document:CdtrAcct/document:Id'
                       '/document:Othr/document:Id', ns) is not None:
            if txdtls.find('.//document:RltdPties/document'
                           ':CdtrAcct/document:Id/document:Othr'
                           '/document:Id', ns) is not None:
                account.append(txdtls.find(
                    './/document:RltdPties/document:CdtrAcct/document:Id'
                    '/document:Othr/document:Id', ns).text)
    for item in account:
        if item not in deduplicated_list:
            deduplicated_list.append(item)
    return deduplicated_list


def getCurrency(root, ns):
    txdtlses = root.findall('.//document:Ntry/document:NtryDtls/document'
                            ':TxDtls', ns)
    account = ''
    for txdtls in txdtlses:
        account = txdtls.find('.//document:RltdPties/document:DbtrAcct'
                              '/document:Id/document:Othr/document:Id',
                              ns)
        if account is not None:
            break
    return account

    """
Takes a xml file in xm 2000 format and trasform it to Bankgiro format
and sends it to database table temp_inputfile
    """


class FileFormatParser:
    def __init__(self):
        super().__init__()
        self.description = 'camt54c plugin'

    def ParsePainFile(self):
        pass

    @staticmethod
    def ParseCreditorFile(xmmfile: object) -> object:
        """
        Parse file takes an camt54C as parameter and transform it to a list
        of sql commands to load into temp_infile.
        :param xmmfile: An xml file.
        :return: A list of sql commands.
        """
        (ntryist, acc, bg) = (None, None, None)
        procparameters = {"proc_kod": "", "o_kod": "", "jour_nr": 0,
                          "procnamn": "", "text": "", "feltyp": "",
                          "errorcode": 99999, "errormessage": ""}
        (ntryno, ntryugno) = (0, 0)
        ConfigObj(os.getcwd() + '/config.ini')
        # Parse XML with ElementTree
        log.info("Starting parsing 54c: %s" % log.Levels.DEBUG)
        # oinitialize some variables.
        rad = 1
        start_post_id = "01"
        slutpost = '70'
        oppningspost = '05'
        insattnings_post = '15'
        betalningspost_ic = '20'
        namnpost_id = '26'
        versionid = '01'.rjust(2)
        format_str = "%Y%m%d%H%M%S"
        start54c_trav_post_rader = list()
        (travno, travsum) = (0, 0)
        (start54c_russ_post_rader, start54c_utl_post_rader) = (list(), list())
        (russno, russsum, totsumm) = (0, 0, 0)
        (delsumma, delsummautl) = (0, 0)
        (utlno, utlsum, errorno) = (0, 0, 0)
        (errorsum, errorsumtot, stackno) = (0, 0, 0)
        (antalpost) = 0
        timestrfile = str(time.strftime(format_str))
        timestr = str(time.strftime('%Y%m%d'))
        # Timestamp, okod and regst
        regts = "to_date('" + str(timestr) + "','yyyy-mm-dd')"
        okod = 'STC'
        " Check if there is a file in the end of the parameter."
        if not exists(str(xmmfile)):
            log.info("No file exists with the name " + str(xmmfile))
            return
        try:
            # Laddar xmlfil
            tree = parse(str(xmmfile))
            root = tree.getroot()
            # For convinience,  init a variable with document.
            ns = {'document': 'urn:iso:std:iso:20022:tech:xsd:camt.054.001.02'}
            # Booking date.
            bookgdate = root.find('.//document:CreDtTm', ns)  # Get the node
            book = parser.parse(bookgdate.text)  # Get the data
            book_str = str(book.date().strftime("%y%m%d"))  # Format
            book_str_long = str(book.date().strftime("%Y%m%d"))  # Format
            # Construct the filename to use.
            # For the filnamn column
            file_name_rad = "'" + book_str + 'bt.bi' + "'"
            temp_filnamn = "'bkstc" + str(book.date().strftime(format_str)) + \
                           ".bi_ok'"  # Filnamn för tepm_filnman,
            # Hämntar bg nummer.
            account = getAccount(root, ns)
            # För vart bg.
            for acc in account:
                # ###############################################################
                # STARTPOST 01
                # ###############################################################
                log.info('camt54C: STARTPOST 01')
                start_post = start_post_id + "BGMAX".ljust(20) + versionid + \
                             timestrfile
                log.debug(start_post)
                # Create insert.
                if acc.startswith('53260873'):
                    start54c_russ_post_rader.append(
                        file_name_rad + "," + str(
                            rad) + ",'" + start_post_id + "','" +
                        start_post + "','" + okod + "'," + regts + ")")
                elif acc.startswith(BankGiroNum.trav.value):
                    start54c_trav_post_rader.append(
                        file_name_rad + "," + str(
                            rad) + ",'" + start_post_id + "','" +
                        start_post + "','" + okod + "'," + regts + ")")
            ntryist = root.findall('.//document:Ntry', ns)
            # <editor-fold desc="Description">
            for ntry in ntryist:
                # #############################################################
                # Entries
                # #############################################################
                stackno += 1
                totsumm += Decimal(ntry.find('.//document:Amt', ns).text)
                # ##############################################################
                # ÖPPNINGSPOST  05
                # ###############################################################
                account = ntry.find('.//document:NtryRef', ns).text
                # Bankgiroinbetalningar.
                if 'BG' in account:
                    ntryno += 1
                    log.info('camt54C: ÖPPNINGSPOST 05')
                    print("NtryRef: " + account)
                    rad += 1
                    splt = account.split()
                    bgito = splt[0].replace('BG', '')
                    accountspl = splt[1]
                    account = accountspl.split('-')
                    account = account[1]
                    currency = str(
                        ntry.find('.//document:Amt', ns).attrib['Ccy'])

                    bankgiro = bgito.rjust(10)
                    plusgiro = ''.ljust(10)
                    valuta = currency.ljust(3)
                    reserv = ''.rjust(55)
                    oppningsp = oppningspost + bankgiro + plusgiro + \
                                valuta + reserv
                    log.debug(oppningsp)
                    if bgito is not None:
                        if bgito.startswith('53260873'):
                            start54c_russ_post_rader.append(
                                file_name_rad + "," + str(
                                    rad) + ",'" + oppningspost + "',"
                                                                 "'" + remove(
                                    oppningsp) + "','" + okod + "'," + regts
                                + ")")
                        elif bgito.startswith(BankGiroNum.trav.value):
                            start54c_trav_post_rader.append(
                                file_name_rad + "," + str(
                                    rad) + ",'" + oppningspost + "',"
                                                                 "'" + remove(
                                    oppningsp) + "','" + okod + "'," + regts
                                + ")")
                    # NtryDtls
                    ntrydtlslist = ntry.findall('.//document:NtryDtls', ns)
                    for ntrydtls in ntrydtlslist:
                        # #################################################################
                        # Entrydetails
                        # #################################################################
                        for txdtls in ntrydtls.findall('.//document:TxDtls',
                                                       ns):
                            # #################################################################
                            # Textdetails
                            # #################################################################
                            bg = txdtls.find(
                                './/document:RltdPties/document:CdtrAcct'
                                '/document:Id/document:Othr/document:Id',
                                ns)  # Trav, russ eller galopp? bg.....
                            if bg is not None:  # Finns det något
                                # bankgiro? Bara för debug.
                                bg = bg.text
                                log.debug('Bankgiro: ' + bg)
                            else:
                                # #############################################
                                # Ohanterade Entrys.
                                # ##################################

                                errorno += 1
                                errorsum = ntry.find('.//document:Amt',
                                                     ns).text
                                errorsumtot += float(errorsum)
                                procparameters["proc_kod"] = "I"
                                procparameters["o_kod"] = "STC"
                                procparameters["jour_nr"] = 0
                                procparameters["procnamn"] = "pyBankRapport " \
                                                             "camt54c"
                                procparameters["feltyp"] = "E"
                                procparameters["errorcode"] = 9999
                                procparameters[
                                    "text"] = "Oidentifierad post " \
                                              + accountspl + ' summa: '\
                                              + errorsum
                                dbClass.CallProcedure('KSP_KRESKLOGGNING'
                                                      '.logga_kresk',
                                                      procparameters, 1)
                                # "kontant Med bankgirot på annan plats,"
                                for refsa in txdtls.findall(
                                    './/document:RmtInf',
                                    ns):
                                    bgraw = refsa.find('.//document:Ustrd',
                                                       ns) \
                                        .text
                                    bg = bgraw.replace('BG', '')
                                    bg = bg.replace('-', '')
                                    log.debug(bg)

                            rltdptieslist = txdtls.findall(
                                './/document:RltdPties', ns)
                            for rltdpties in rltdptieslist:
                                rad += 1
                                # ##############################################################
                                # 	20	BETALNINGSPOST
                                # ##############################################################
                                log.info('camt54C: BETALNINGSPOST 20')
                                antalpost += 1
                                refs = txdtls.find('.//document:Refs', ns)
                                refnrc = refs.find('.//document:InstrId',
                                                   ns)
                                refnr = refnrc.text
                                summa = txdtls.find(
                                    './/document:AmtDtls/document:TxAmt'
                                    '/document:Amt',
                                    ns).text
                                amount_ore = Decimal(math.trunc(
                                    Decimal(summa) * 100))
                                delsumma += Decimal(summa)  # Summering.
                                send_bankgironummer = ''.rjust(10, '0')
                                send_referens = refnr.rjust(25)
                                send_betalningsbelopp = str(
                                    amount_ore).rjust(18, '0')
                                send_referenskod = ''.ljust(1)
                                send_betalningskanalkod = '1'.ljust(1)
                                send_lopnummer = ''.ljust(12)
                                avibildmarkering = ''.ljust(1)
                                send_blanka = ''.ljust(10)
                                send = send_bankgironummer + \
                                       send_referens + \
                                       send_betalningsbelopp + \
                                       send_referenskod + \
                                       send_betalningskanalkod + \
                                       send_lopnummer + \
                                       avibildmarkering + send_blanka
                                betalningspost = betalningspost_ic + send
                                log.debug(betalningspost)
                                if bg.startswith('53260873'):
                                    russno += 1
                                    russsum += amount_ore
                                    start54c_russ_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'20','" +
                                        betalningspost + "','" + okod +
                                        "'," + regts + ")")
                                else:
                                    travno += 1
                                    travsum += amount_ore
                                    start54c_trav_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'20','" +
                                        betalningspost + "','" + okod +
                                        "'," + regts + ")")
                                # End tkx
                                # ###############################################################
                                # NAMNPOST 26
                                # ###############################################################
                                log.info('camt54C: NAMNPOST 26')
                                rad += 1
                                if rltdpties.find(
                                    './/document:Dbtr/document:Nm',
                                    ns) is not None:
                                    betnamn = rltdpties.find(
                                        './/document:Dbtr/document:Nm',
                                        ns).text.ljust(35)
                                else:
                                    betnamn = ''.ljust(35)
                                ext_namn = ''.ljust(35)
                                extra = ''.ljust(8)
                                namnpost26 = namnpost_id + betnamn + \
                                             ext_namn + extra
                                log.debug(namnpost26)

                                if bg.startswith('53260873'):
                                    start54c_russ_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'" + namnpost_id +
                                        "','" + remove(
                                            namnpost26) + "','" + okod +
                                        "'," + regts + ")")
                                else:
                                    start54c_trav_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'" + namnpost_id +
                                        "','" + remove(
                                            namnpost26) + "','" + okod +
                                        "'," + regts + ")")
                                # ###############################################################
                                # ADRESSPOST 1 27
                                # ###############################################################
                                log.info('camt54C: ADRESSPOST 27')
                                rad += 1
                                bet_adress = rltdpties.find(
                                    './/document:Dbtr/document:PstlAdr'
                                    '/document:StrtNm',
                                    ns)
                                bet_zip = rltdpties.find(
                                    './/document:Dbtr/document:PstlAdr'
                                    '/document:PstCd',
                                    ns)
                                if bet_adress is not None:
                                    bet_adress = bet_adress.text.ljust(35)
                                else:
                                    bet_adress = ' '.ljust(35)
                                if bet_zip is not None:
                                    bet_zip = bet_zip.text.ljust(9)
                                else:
                                    bet_zip = ''.ljust(9)
                                bet_res = ' '.ljust(34)
                                adress27 = bet_adress + bet_zip + bet_res
                                if adress27 is not None:
                                    adress27 = '27'
                                log.debug(adress27)
                                if bg.startswith('53260873'):
                                    start54c_russ_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'27','" + remove(
                                            adress27) + "','" + okod +
                                        "'," + regts + ")")
                                else:
                                    start54c_trav_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'27','" + remove(
                                            adress27) + "','" + okod +
                                        "'," + regts + ")")
                                # ###############################################################
                                # ADRESSPOST 2 28
                                # ###############################################################
                                log.info('camt54C: ADRESSPOST 28')
                                rad += 1
                                bet_ort = '28'.ljust(35)
                                bet_countr = ' '.ljust(35)
                                bet_countrcode = ''.ljust(2)
                                bet_ort_res = ''.ljust(6)
                                adress28 = bet_ort + bet_countr + \
                                           bet_countrcode + bet_ort_res
                                log.debug(adress28)
                                if bg.startswith('53260873'):
                                    start54c_russ_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'28','" + remove(
                                            adress28) + "','" + okod +
                                        "'," + regts + ")")
                                else:
                                    start54c_trav_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'28','" + remove(
                                            adress28) + "','" + okod +
                                        "'," + regts + ")")
                                # ###############################################################
                                # ORGANISATIONSNUMMERPOST 29
                                # ###############################################################
                                log.info('camt54C: ADRESSPOST 29')
                                rad += 1
                                bet_orgnr = ''.ljust(12)
                                bet_org_res = ''.ljust(66)
                                adress29 = '29' + bet_orgnr + bet_org_res
                                log.debug(adress29)
                                if bg.startswith(
                                    '53260873'):
                                    start54c_russ_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'29','" +
                                        adress29 + "','" + okod + "',"
                                                                  "" +
                                        regts + ")")
                                else:
                                    start54c_trav_post_rader.append(
                                        file_name_rad + "," + str(
                                            rad) + ",'29','" +
                                        adress29 + "','" + okod + "',"
                                                                  "" +
                                        regts + ")")
                        # #################################################################
                        # INSÄTTNINGSPOST 15
                        # 'Mottagarens bankkontonummer + Betalningsdag +
                        # inslöpnr
                        # + belopp + valuta + antal +t yp
                        # #################################################################
                        log.info('camt54C: Bankgiro INSÄTTNINGSPOST 15')
                        rad += 1
                        bgsumma = math.trunc(Decimal(delsumma) * 100)
                        bankkontonummer = account[2:account.find(
                            '')].strip().rjust(35, '0')
                        betalningsdag = book_str_long.strip().ljust(8, '0')
                        # inslopnr = ntry.find('.//document:NtryRef',
                        # ns).text
                        inslopnr = '00000'.rjust(5, '0')
                        belopp = str(bgsumma).rjust(18, '0')
                        valuta = 'SEK'.ljust(3)
                        antalins = str(antalpost).rjust(8, '0')
                        insattningsrad = insattnings_post.ljust(
                            2) + bankkontonummer + betalningsdag + \
                                         inslopnr + \
                                         belopp + valuta + antalins
                        log.debug(insattningsrad)
                        log.info('delsumma:' + str(delsumma))
                        if bg.startswith('53260873') and delsumma > 0:
                            start54c_russ_post_rader.append(
                                file_name_rad + "," + str(
                                    rad) + ",'" + insattnings_post + "',"
                                                                     "'" +
                                insattningsrad + "','" + okod + "',"
                                                                "" +
                                regts + ")")
                            delsumma = 0;
                        elif bg.startswith(
                            BankGiroNum.trav.value) and delsumma > 0:
                            start54c_trav_post_rader.append(
                                file_name_rad + "," + str(
                                    rad) + ",'" + insattnings_post + "',"
                                                                     "'" +
                                insattningsrad + "','" + okod + "',"
                                                                "" +
                                regts + ")")

                        delsumma = 0  # Nollställning
                        # </editor-fold>
                # End bg
                else:
                    ntrydtlslist = ntry.findall('.//document:NtryDtls', ns)
                    for ntrydtls in ntrydtlslist:
                        for txdtls in ntrydtls.findall(
                            './/document:TxDtls', ns):
                            rltdptieslist = txdtls.findall(
                                './/document:RltdPties', ns)
                            for rltdpties in rltdptieslist:
                                log.debug("Utlands inbetalning")

                                refs = txdtls.find('.//document:Refs', ns)
                                refnrc = refs.find('.//document:InstrId',
                                                   ns)
                                if refnrc is not None:
                                    refnr = refnrc.text
                                else:
                                    refnr = ''
                                peng = txdtls.find(
                                    './/document:AmtDtls/document:TxAmt'
                                    '/document:Amt',
                                    ns)
                                if peng is not None:  # SEK
                                    summa = peng.text
                                else:  # EURO
                                    summa = ''  # txdtls.find(

                                utlno += 1
                                rad += 1
                                amount_ore = math.trunc(
                                    Decimal(summa) * 100)
                                log.debug(amount_ore)
                                utlsum += Decimal(amount_ore)
                                send_bankgironummer = ''.rjust(10, '0')
                                send_referens = refnr[:25].rjust(25)
                                send_betalningsbelopp = str(
                                    amount_ore).rjust(18, '0')
                                send_referenskod = ''.ljust(1)
                                send_betalningskanalkod = '1'.ljust(1)
                                send_lopnummer = ''.ljust(12)
                                avibildmarkering = ''.ljust(1)
                                send_blanka = ''.ljust(6)
                                send = send_bankgironummer + \
                                       send_referens + \
                                       send_betalningsbelopp + \
                                       send_referenskod + \
                                       send_betalningskanalkod + \
                                       send_lopnummer + \
                                       avibildmarkering + send_blanka
                                betalningspost = betalningspost_ic + send
                                # ############################################################
                                # 20 post
                                # ############################################################
                                start54c_utl_post_rader.append(
                                    file_name_rad + "," + str(
                                        rad) + ",'20','" +
                                    betalningspost + "','" + okod +
                                    "'," + regts + ")")
                                # ############################################################
                                # NAMNPOST 26
                                # ############################################################
                                log.info('camt54C: NAMNPOST 26')
                                rad += 1
                                if rltdpties.find(
                                    './/document:Dbtr/document:Nm',
                                    ns) is not None:
                                    betnamn = rltdpties.find(
                                        './/document:Dbtr/document:Nm',
                                        ns).text.ljust(35)
                                else:
                                    betnamn = ''.ljust(35)
                                ext_namn = ''.ljust(35)
                                extra = ''.ljust(8)
                                namnpost26 = namnpost_id + betnamn + \
                                             ext_namn + extra
                                log.debug(namnpost26)
                                start54c_utl_post_rader.append(
                                    file_name_rad + "," + str(rad) + ",'" +
                                    namnpost_id + "',q'[" + remove(
                                        namnpost26) + "]','" +
                                    okod + "'," + regts + ")")
                                # ############################################################
                                # ADRESSPOST 1 27
                                # ############################################################
                                log.info('camt54C: ADRESSPOST 27')
                                rad += 1
                                bet_adress = rltdpties.find(
                                    './/document:Dbtr/document:PstlAdr'
                                    '/document:StrtNm',
                                    ns)
                                bet_zip = rltdpties.find(
                                    './/document:Dbtr/document:PstlAdr'
                                    '/document:PstCd',
                                    ns)
                                if bet_adress is not None:
                                    bet_adress = bet_adress.text.ljust(35)
                                else:
                                    bet_adress = ' '.ljust(35)
                                if bet_zip is not None:
                                    bet_zip = bet_zip.text.ljust(9)
                                else:
                                    bet_zip = ''.ljust(9)
                                bet_res = ' '.ljust(34)
                                adress27 = bet_adress + bet_zip + bet_res
                                if adress27 is not None:
                                    adress27 = '27'

                                start54c_utl_post_rader.append(
                                    file_name_rad + "," + str(
                                        rad) + ",'27',q'[" + remove(
                                        adress27) + "]','" + okod + "',"
                                                                    "" +
                                    regts + ")")
                                # ###########################################################
                                # ADRESSPOST 2 28
                                # ###########################################################
                                log.info('camt54C: ADRESSPOST 28')
                                rad += 1
                                bet_ort = '28'.ljust(35)
                                bet_countr = ' '.ljust(35)
                                bet_countrcode = ''.ljust(2)
                                bet_ort_res = ''.ljust(6)
                                adress28 = bet_ort + bet_countr + \
                                           bet_countrcode + bet_ort_res
                                log.debug(adress28)

                                start54c_utl_post_rader.append(
                                    file_name_rad + "," + str(
                                        rad) + ",'28','" + remove(
                                        adress28) + "','" + okod + "',"
                                                                   "" +
                                    regts + ")")
                                # ###########################################################
                                # ORGANISATIONSNUMMERPOST 29
                                # ###########################################################
                                log.info('camt54C: ADRESSPOST 29')
                                rad += 1
                                bet_orgnr = ''.ljust(12)
                                bet_org_res = ''.ljust(66)
                                adress29 = '29' + bet_orgnr + bet_org_res
                                log.debug(adress29)
                                start54c_utl_post_rader.append(
                                    file_name_rad +
                                    "," + str(rad) + ",'29','" +
                                    adress29 + "','" + okod + "',"
                                                              "" + regts
                                    + ")")

                            log.info('camt54C: utl INSÄTTNINGSPOST 15')
                            rad += 1
                            delsummautl = math.trunc(
                                Decimal(amount_ore))
                            bankkontonummer = account[2:account.find(
                                '')].strip().rjust(35, '0')
                            betalningsdag = book_str_long.strip().ljust(8,
                                                                        '0')
                            # inslopnr = ntry.find('.//document:NtryRef',
                            # ns).text
                            inslopnr = '00000'
                            belopp = str(delsummautl).rjust(18, '0')
                            valuta = 'SEK'.ljust(3)
                            antalins = str(antalpost).rjust(8, '0')
                            insattningsrad = insattnings_post.ljust(
                                2) + bankkontonummer + betalningsdag + \
                                             inslopnr + \
                                             belopp + valuta + antalins
                            log.debug(insattningsrad)
                            log.info('delsummautl:' + str(delsummautl))
                            if delsummautl > 0:
                                start54c_utl_post_rader.append(
                                    file_name_rad + "," + str(
                                        rad) + ",'" + insattnings_post +
                                    "',"
                                    "'" +
                                    insattningsrad + "','" + okod + "',"
                                                                    "" +
                                    regts + ")")
                                delsummautl = Decimal(0)


            else:
                ntryugno += 1
                print("Fel")
            # End Ntry
            # ###############################################################
            # SLUTPOST 70
            # ###############################################################
            log.info('camt54C: SLUTPOST 70')
            rad += 1
            sumpost = str(russno).zfill(8) + str('').zfill(8) + ''.ljust(
                8, '0') + ''.ljust(8, '0')
            sumeringspost = slutpost + sumpost
            start54c_russ_post_rader.append(file_name_rad + "," + str(
                rad) + ",'" + slutpost + "','" + sumeringspost + "',"
                                                                 "'" + okod
                                            + "'," + regts + ")")
            # ###############################################################
            sumpost = str(travno + utlno).zfill(8) + str('').zfill(
                8) + ''.ljust(
                8, '0') + ''.ljust(8, '0')
            sumeringspost = slutpost + sumpost
            start54c_trav_post_rader.append(file_name_rad + "," + str(
                rad) + ",'" + slutpost + "','" + sumeringspost + "',"
                                                                 "'" + okod
                                            + "'," + regts + ")")

            # ##################################################################

            regist_fil = temp_filnamn + "," + regts + ")"
            table = "temp_inbetfil"
            log.debug('startar rader')
            # #################################################################
            # Från ören till Kronor.
            # #################################################################
            reftotno = utlno + travno + russno + errorno  # Antal poster
            travsumsek = float(travsum / 100)
            utlsumsek = float(utlsum / 100)
            russsumsek = float(russsum / 100)
            reftot = float(
                utlsumsek + russsumsek + travsumsek + errorsumtot)  # Totalsum
            delta = float(
                totsumm) - reftot  # Delta mellan beräknad och xml värde
            log.info("# #####################################################")
            log.info("# Summering av körning")
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
            # ##################################################################
            # Startar databas jobb för stora hästar
            # ##################################################################
            log.debug('Processar trav... ')
            no = 1  # Sport
            if start54c_trav_post_rader is not None:
                travrader = list(
                    OrderedDict.fromkeys(start54c_trav_post_rader))
                dbClass.remove_temp_filesname(temp_filnamn, no=no)
                dbClass.remove_temp_utbetfil(file_name_rad, table_name=table,
                                             no=no)
                dbClass.db_insert_temp_filnamn(datem=regist_fil, no=no)
                dbClass.db_execution(start_post_rader=travrader,
                                     table_name=table, no=no)
            # ###################################################################
            # Startar jobb för russ
            # ###################################################################
            log.debug('Processar russ... ')
            no = 2  # russ
            if start54c_russ_post_rader is not None:
                russrader = list(
                    OrderedDict.fromkeys(start54c_russ_post_rader))
                dbClass.remove_temp_filesname(temp_filnamn, no=no)
                dbClass.remove_temp_utbetfil(file_name_rad, table_name=table,
                                             no=no)
                dbClass.db_insert_temp_filnamn(datem=regist_fil, no=no)
                dbClass.db_execution(start_post_rader=russrader,
                                     table_name=table, no=no)
            # #####################################################################
            # Startar jobb för utlandsbetalingar
            # #####################################################################
            log.debug('Processar Utlands... ')
            no = 1  # Utl
            if len(start54c_utl_post_rader) != 0:
                utlandsrader = list(
                    OrderedDict.fromkeys(start54c_utl_post_rader))
                # dbClass.remove_temp_filesname(temp_filnamn, no=no)
                # dbClass.remove_temp_utbetfil(file_name_rad, table_name=table,
                #                             no=no)
                # dbClass.db_insert_temp_filnamn(datem=regist_fil, no=no)
                dbClass.db_execution(start_post_rader=utlandsrader,
                                     table_name=table, no=no)
        except ValueError as e:
            log.error("ParseCreditorFile Error: " + str(e))
            raise ValueError("ParseCreditorFile Error: " + str(e))
        except ParseError as err:
            log.error('ParseCreditorFile Error: ' + str(err))
        except (
            FileNotFoundError, TypeError, RuntimeError, KeyError,
            NameError,
            IOError, NotImplementedError,
            SyntaxError) as err:
            log.error('ParseCreditorFile Error: ' + str(err))
        except Exception as err:
            log.error("ParseCreditorFile Error: " + str(err))
        finally:
            log.info('ParseCreditorFile info: cam54bt done')
