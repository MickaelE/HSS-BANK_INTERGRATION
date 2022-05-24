import math
import os
from datetime import datetime
import time
from itertools import cycle
from os.path import exists
from dateutil import parser
from xml.etree.ElementTree import parse, ParseError
from collections import OrderedDict
import bankfiler.DBclass as dbclass
from decimal import Decimal
from configobj import ConfigObj
from global_logger import Log
log = Log.get_logger(logs_dir='logs')


def remove(string):
    return string.replace(" ", "")


def get_filename(path):
    basename = os.path.basename(path)
    basename = basename[:12]
    return basename


def exsisting_rownr(ntrydtls):
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
    try:
        desired_array = [int(numeric_string) for numeric_string in arr]
        num = num + 1
        while num in desired_array:
            num = num + 1
        desired_array.append(num)
    except (Exception,):
        log.info("no get_rownum")
        num = 0
    finally:
        return num


def convert_int(number, decimals):
    return str(number).zfill(decimals)


class InputsClass:
    @staticmethod
    def parsecam54(file_name: object) -> object:
        deduplicated_list = ""
        ConfigObj(os.getcwd() + '/config.ini')
        # Parse XML with ElementTree
        log.info("Startar rapport: %s" % log.Levels.INFO)
        rad = 0
        start_post_id = "11"
        aviserings_post_id = "14"
        customer_id = "26"
        kontonummerpost_id = "40"
        amount = "''"
        kundid = "''"
        format_str = "%Y%m%d%H%M%S"
        start_post_rader = list()
        timestr = str(time.strftime("%y%m%d"))

        if not exists(file_name):
            log.info("No file exists with the name " + file_name)
            return
        tree = parse(file_name)
        try:
            root = tree.getroot()
            ns = {'document': 'urn:iso:std:iso:20022:tech:xsd:camt.054.001.02'}
            # Iban/Account
            # account = root.find('.//document:Acct/document:Id/document:Othr/document:Id', ns)
            iban = root.find('.//document:Acct/document:Id/document:IBAN', ns)

            curr = root.find('.//document:Acct/document:Ccy', ns)
            if curr:
                curr = curr.text
            else:
                curr = ""
            TxsSummryno = root.find('.//document:TxsSummry/document:TtlDbtNtries/document:NbOfNtries', ns).text
            TxsSummrysum = str(math.trunc(
                Decimal(root.find('.//document:TxsSummry/document:TtlDbtNtries/document:Sum', ns).text) * 100))
            # Booking date.
            bookgdate = root.find('.//document:CreDtTm', ns)

            book = parser.parse(bookgdate.text)
            book_str = str(book.date().strftime("%y%m%d"))
            file_name_rad = "'" + book_str + 'bt.ret' + "'"
            temp_filnamn = 'bkstc' + str(book.strftime(format_str)) + 'bt.ret' + "'"
            txdtls = root.find('.//document:Ntry/document:NtryDtls/document:TxDtls', ns)
            account = txdtls.find('.//document:RltdPties/document:DbtrAcct/document:Id/document:Othr/document:Id',
                                  ns)
            if account:
                account = account.text
            else:
                account = ''

            start_post = start_post_id + '00' + account + book_str + "LEVERANTÖRSBETALNINGAR" + book_str + curr
            # FILNAMN, RADNR, INFORMATION, P_ID,BELOPP,BNKTO_ID,REGTS
            regts = "to_date('" + str(book.date()) + "','yyyy-mm-dd')"
            # Start post
            start_post_rader.append(
                file_name_rad + ",'" + str(rad) + "','" + remove(start_post) + "'," + kundid + "," + amount +
                "," + regts + ")")
            ################################################
            # post 29 math.trunc(Decimal(amt.text) * 100)
            #################################################
            summpost = '29' + account.zfill(10) + TxsSummryno.zfill(8) + TxsSummrysum.zfill(12)
            start_post_rader.append(
                file_name_rad + ",'" + str(100) + "','" + remove(summpost) + "'," + kundid + "," + amount +
                "," + regts + ")")
            # NtryDtls
            txdtlslist = root.findall('.//document:Ntry/document:NtryDtls/document:TxDtls', ns)
            existing = exsisting_rownr(txdtlslist)
            # Notification
            for txdtls in txdtlslist:
                instrid = txdtls.find('.//document:Refs/document:InstrId', ns)
                # References aviserings_post_id
                bokf_dat = ""
                row_id = 0
                if instrid is not None:
                    pmtinfid = instrid.t9ext.split('-')
                    bokf_dat = pmtinfid[1]
                else:
                    cycle()
                row_cust_id = txdtls.find('.//document:Refs/document:EndToEndId', ns)
                if row_cust_id is not None:
                    row_cust_id = row_cust_id.text.split('-')
                    row_id = row_cust_id[1].zfill(10)
                    kundid = row_cust_id[0].zfill(9)
                for node in txdtls.findall('.//document:CdtrAcct/', ns):
                    print(node.tag, node.attrib, node.text)
                if bokf_dat:
                    bokf_dat = datetime.strptime(bokf_dat, format_str)
                else:
                    bokf_dat = ''

                utbetalningsnr = txdtls.find('.//document:CdtrAcct/document:Id/document:Othr/document:Id', ns)
                if utbetalningsnr is not None:
                    utbetalningsnr = utbetalningsnr.text[0: 8]
                    utbetalningsnr = utbetalningsnr.zfill(9)
                else:
                    utbetalningsnr = '1'
                amt = txdtls.find('.//document:AmtDtls/document:TxAmt/document:Amt', ns)
                avinr = txdtls.find('.//document:RmtInf/document:Ustrd', ns)

                amount_ore = math.trunc(Decimal(amt.text) * 100)
                # Aviseringspost(14): Utbetalningsnr Kundnr Avinr Belopp i ören Bokföringsdatum
                utbetalningsnr = utbetalningsnr.zfill(9)
                fill = 22 - len(aviserings_post_id)
                avi = avinr.text.zfill(16)
                avi1 = avi.zfill(fill + 15 - len(utbetalningsnr))
                amount_ore_len = str(amount_ore).zfill(12)
                cdtracct = txdtls.find('.//document:CdtrAcct', ns)
                bet = aviserings_post_id + utbetalningsnr + avi1 + amount_ore_len
                aviserings_rad = file_name_rad + ",'" + str(row_id) + "','" + bet + "'" + ",'" + kundid + "'," + str(
                    amount_ore) + "," + "to_date('" + bokf_dat.strftime(
                    "%y%m%d") + "','yymmdd')" + ")"

                start_post_rader.append(aviserings_rad)
                # Bankkontoinsättning utan avisering(40, 14) BGNR BBAN
                prtry = txdtls.find('.//document:RltdPties/document:DbtrAcct/document:Id/document:Othr'
                                    '/document:SchmeNm/document:Prtry', ns)
                # if prtry.text == "BBAN":

                # Kontonummerpost(40): Löpnr. Clearingnr  Kontonr.
                rad = get_rownum(rad, existing)
                #  kontonummerpost_rad = file_name_rad + ",'" + str(rad).zfill(10) + "','" + kontonummerpost_id + convert_int(row_id, 10) + "',''," + amount + "," + "to_date('" + bokf_dat.strftime("%y%m%d") + "','yymmdd')" + ") "

                # start_post_rader.append(kontonummerpost_rad)
                # --------------------------------------------------
                #  Kontonummerpost(26)
                # --------------------------------------------------
                cdtracct = txdtls.find('.//document:CdtrAcct', ns)
                cred_name = txdtls.find('.//document:Cdtr/document:Nm', ns)
                if cdtracct is not None:  # Nordea seems to not use this often.
                    # cdrid = txdtls.find('.//document:CdtrAcct/document:Id', ns)
                    creditor = "'" + customer_id + row_id + " " + cred_name.text + "'"

                    rad = get_rownum(rad, existing)
                    # Kund 26 Löpnr, Namn ev CO-adress
                    kund_rad = file_name_rad + ",'" + str(rad).zfill(
                        10) + "'," + creditor + ",'" + kundid + "'," + amount + "," + "to_date('" + \
                               bokf_dat.strftime(format_str) + "','yyyymmddhh24miss')" + ") "

                    start_post_rader.append(kund_rad)
                else:
                    #  Adresspost(27)
                    rad = get_rownum(rad, existing)
                    avipost = '27' + str(rad).zfill(11) + cred_name.text
                    avi_rad = file_name_rad + "," + str(rad).zfill(
                        10) + ",'" + avipost + "'," + amount + ",''," + "to_date('" + bokf_dat.strftime(
                        format_str) + "', 'yyyymmddhh24miss')" + ") "
                    start_post_rader.append(avi_rad)
            rader = list(OrderedDict.fromkeys(start_post_rader))
            regist_fil = "'" + temp_filnamn + "," + "to_date('" + book.strftime(
                format_str) + "', 'yyyymmddhh24miss')" + ") "
            dbclass.db_insert_temp_filnamn(datem=regist_fil)
            dbclass.db_execution(start_post_rader=rader)
            get_files = os.listdir(file_source)

            for g in get_files:
                shutil.move(file_source + g, file_destination)
        except ValueError as e:
            log.error(e)
            raise ValueError(e)
        except ParseError:
            print(deduplicated_list)
        except (FileNotFoundError, TypeError, RuntimeError, KeyError, NameError, IOError, NotImplementedError,
                SyntaxError) as err:
            print('The file is not present.' + str(err))
        except Exception as err:
            log.error(str(err))
        finally:
            log.info('cam54bt done')
            return 0

    @classmethod
    def Inparsecam54(cls, xmlfile):
        pass
