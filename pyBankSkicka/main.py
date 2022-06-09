# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import BankSkicka.QueueUtils
from global_logger import Log
from BankSkicka.QueueUtils import QueueUtil
from SecureEnvelope import SecureEnvelope

log = Log.get_logger(logs_dir='logs')
"""
Author: Mickael Eriksson, Miracle42 2021
Skript som hanterar att skapa secure_enevelope av utbetalningsfil.
Licens: MIT
"""

if __name__ == '__main__':
    log.info('######################################################')
    log.info('pyBankSkicka version 0.1.2')
    log.info('######################################################')
    log.debug('pyBankSkicka version 0.1.2')
    QueueUtil.getQueue()
