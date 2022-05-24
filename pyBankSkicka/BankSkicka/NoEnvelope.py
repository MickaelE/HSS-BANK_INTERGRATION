#  Copyright (c) 2022. Mickael Eriksson
from configobj import ConfigObj, ConfigObjError, ConfigspecError
from paramiko.ssh_exception import SSHException
from BankSkicka.Communication import Communication
import xml.etree.ElementTree as Et
from datetime import datetime
from global_logger import Log
from MickeNet.PyGPGlib import PyGpgLib
import time
import os

# #####################################################
# author= “Mickael Eriksson”
# copyright = “Copyright 2021, Travsport”
# credits = [“Mickael Eriksson”]
# license = “MPL 2.0”
# version = “0.1.0”
# maintainer = “Mickael Eriksson”
# email= “mickael.eriksson@travsport.se”
# status = “Dev”
# #####################################################
# {code}

log = Log.get_logger(logs_dir='logs')


class NoEnvelope:
    @staticmethod
    def __createXML__(content_string):
        """
        Create a xml file that coheres to the secure envelope standard
        :param content_string: A string (xml)
        :return: secure_envelope xml
        """
        global retval
        bolag = ''  # CustomerUtil.getCurrCust(content_string)
        config = ConfigObj(os.getcwd() + '/config.ini')
        gpghome = config['cert']['gpghome']
        gpgbin = config['cert']['gpgbin']
        pwd = config['cert']['password']
        # content_string =  content_string.read()

        pygpglib = PyGpgLib(gpghome, gpgbin)
        content_string_file = config['misc']['outdir'] + '/' + datetime.now().strftime(
            "%Y%m%d-%H%M%S") + '_noenvelope_trav.xml'
        envelope_file = config['misc']['outdir'] + '/' + datetime.now().strftime("%Y%m%d-%H%M%S") + '_trav.xml'
        with open(content_string_file, 'w',encoding='utf8') as content:
            content.write(content_string)
        envelope_file_sing = config['misc']['outdir']
        _id = "123456"
        date_time = datetime.fromtimestamp(time.time())
        _date = date_time.strftime('%Y-%m-%dT%H:%M:%S%Z%z')
        retval = pygpglib.sign_content(content_string_file, pwd, envelope_file_sing, 'gpg')
        # Digital sign orginal
        log.debug(retval)
        log.debug("signed")
        try:
            # Sending the data...
            if bolag == 'SGC':
                sfthost = config['sftp1']['host']
                sftpuser = config['sftp1']['username']
                sftppw = config['sftp1']['password']
                bank_dir = config['sftp1']['bank_dir']
                envelope = config['sftp1'].as_bool('envelope')
                private_key = config['sftp1']['private_key']
            else:
                sfthost = config['sftp2']['host']
                sftpuser = config['sftp2']['username']
                sftppw = config['sftp2']['password']
                bank_dir = config['sftp2']['bank_dir']
                envelope = config['sftp2'].as_bool('envelope')
                private_key = config['sftp2']['private_key']
            log.info("Trying to send to sftp")
            communication = Communication(sfthost, sftpuser, sftppw, bank_dir, private_key)
            if envelope:
                communication.__send__(retval)
            else:
                communication.__send__(retval)
            retval = 0
        except (RuntimeError, TypeError, NameError, ValueError, IOError, IndexError) as err:
            log.error('EnvelopeError ..' + str(err))
        except (ConfigObjError, ConfigObjError, ConfigspecError) as Conferr:
            log.error('EnvelopeError ..' + str(Conferr))
        except SSHException as wee:
            log.error('EnvelopeError.. ' + str(wee))
        except Exception as ecj:
            log.error('EnvelopeError.. ' + str(ecj))
        finally:
            return retval
