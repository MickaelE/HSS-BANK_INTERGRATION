#  Copyright (c) 2022. Mickael Eriksson
import datetime
import argparse
# Other Libs
import logging

import lxml
from global_logger import Log
from lxml import etree

log = Log.get_logger(logs_dir='logs')


# {code}
def getCurrCust(bfile):
    global custname
    try:
        nsmap = {'document': 'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03',
                 'ns': 'http://www.w3.org/2001/XMLSchema-instance'}

        _payload = ''.join([str(item) for item in bfile])

        payload = etree.fromstring(bytes(bfile, encoding='utf8'))
        _custname = payload.xpath('/document:Document/document:CstmrCdtTrfInitn/document:GrpHdr/document:InitgPty'
                                  '/document:Nm', namespaces=nsmap)
        custname = _custname[0].text
    except etree.XMLSyntaxError as parseerr:
        log.info(' ungnown EnvelopeError ..')
    except etree.ParseError as parseerr:
        log.info(' ungnown EnvelopeError ..')
    except etree.ParserError as parseerr:
        log.info(' ungnown EnvelopeError ..')
    except (Exception,):
        log.info(' ungnown EnvelopeError ..')
    return custname
