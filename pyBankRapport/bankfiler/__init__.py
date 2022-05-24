import logging
import os
import time

from MickeNet.PyGPGlib import PyGpgLib
from global_logger import Log
from timeloop import Timeloop
from datetime import timedelta
from bankfiler.FtpWatcher import FtpWatcher
from configobj import ConfigObj
from global_logger import Log
tl = Timeloop()
log = Log.get_logger(logs_dir='logs')


def main():
    # if __name__ == "__main__":
    try:
        config = ConfigObj(os.getcwd() + '/config.ini')
        _path = config["misc"]["outdir"]
        gpghome = config['cert']['gpghome']
        gpgbin = config['cert']['gpgbin']
        pwd = config['cert']['password']
        print("-" * 25)
        print("Reporting tool 0.1.2")
        print("-" * 25)
        logging.debug("Starting using " + _path)

        @tl.job(interval=timedelta(minutes=1))
        def sample_job_every_2s():
            ftpwatcher = FtpWatcher(host=config["seb"]["host"], username=config["seb"]["username"],
                                    password=config["seb"]["password"], bank_dir=config["seb"]["bank_dir"],
                                    localfile=config["seb"]["localfile"], filepattern=config["seb"]["filepattern"],
                                    private_key=config["seb"]["private_key"], gpghome=gpghome, gpgbin=gpgbin)
            ftpwatcher.watch()
            print("60s job current time : {}".format(time.ctime()))

        # running observer
        tl.start(block=False)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tl.stop()
    except Exception as ex:
        tl.stop()
