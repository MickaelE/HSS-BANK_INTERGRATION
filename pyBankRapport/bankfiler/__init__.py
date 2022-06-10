#!/usr/bin/env python3
# -*- coding: utf-8 -*- L
# ----------------------------------------------------------------------------
# Created By  : Mickael Eriksson
# Created Date: 20220421
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Start of app.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import logging
import os
import time
from datetime import timedelta

from configobj import ConfigObj
from global_logger import Log
from timeloop import Timeloop

from bankfiler.FtpWatcher1 import FtpWatcher

tl = Timeloop()
log = Log.get_logger(logs_dir='logs')


def main():
    # if __name__ == "__main__":
    # Plugin mananger
   #  my_plugins = PluginCollection('plugins')

    try:
        config = ConfigObj(os.getcwd() + '/config.ini')
        _path = config["misc"]["outdir"]
        gpghome = config['cert']['gpghome']
        gpgbin = config['cert']['gpgbin']
        pwd = config['cert']['password']
        log.info("=" * 25)
        log.info("pyBankRapport 0.1.3")
       # log.info("Installed plugins: " + str(my_plugins.plugins.text))
        log.info("=" * 25)
        logging.debug("Starting using " + _path)

        @tl.job(interval=timedelta(minutes=1))
        def ftp_job_every_60s():
            ftpwatcher = FtpWatcher(host=config["seb"]["host"], username=config["seb"]["username"],
                                    password=config["seb"]["password"], bank_dir=config["seb"]["bank_dir"],
                                    localfile=config["seb"]["localfile"], filepattern=config["seb"]["filepattern"],
                                    private_key=config["seb"]["private_key"], gpghome=gpghome, gpgbin=gpgbin)
            ftpwatcher.watch()
            log.info("60s job current time : {}".format(time.ctime()))

        # running observer
        tl.start(block=False)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tl.stop()
    except Exception as ex:
        tl.stop()
