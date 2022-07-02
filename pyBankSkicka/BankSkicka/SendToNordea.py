#  Copyright (c) 2022. Mickael Eriksson
from configobj import ConfigObj, ConfigObjError, ConfigspecError
from paramiko.ssh_exception import SSHException
from datetime import datetime
from global_logger import Log

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
from pyBankSkicka.BankSkicka.ftpClient import SftLib
log = Log.get_logger(logs_dir='logs')


class SendToNordea:
    @staticmethod
    def createXML(content_string):
        """
        Create a xml file that coheres to the secure envelope standard
        :param content_string: A string (xml)
        :return: secure_envelope xml
        """
        keyfiletype = None
        date = datetime.now().strftime("%Y%m%d%I%M%S")
        customer_id = '123456'
        command = 'UploadFile'
        timestamp = '2015-03-23T11:51:26.993+01:00'
        environment = 'PRODUCTION'
        targetid = '5780860238'
        softwareid = 'WTSSWebServices'
        filetype = 'NDCAPXMLI'
        content = content_string
        digest_value = 'pRE4OEvO6/2lskhDBqWyOC0axiM='
        signature_value = 'Vfk2JDSVodavcNGPua8WWWaNl' \
                          '/L7bgne9KLwF9zE7Nx6gFSepDhKSvI8y' \
                          '+5tFVLNfwFx9XNuqkfDrcrddQb+XWB5R6pz3ugP' \
                          '/aLpm46BMaM3twP5AkCkhvJvOoavEBYLRAwjLzL1KD' \
                          '+OQpYc1pXffRGEnSHBCZH/vxNIribycBI='
        x509_issuer_name = 'SERIALNUMBER=516406-0120, CN=Nordea Corporate CA ' \
                           '' \
                           '' \
                           '01, O=Nordea Bank AB (publ), C=SE '
        x509_serial_number = '24988089'
        x509_certificate = 'MIIDwTCCAqmgAwIBAgIEAX1JuTANBgkqhkiG9w0BAQUFADBk' \
                           'MQswCQYDVQQGEwJTRTEeMBwGA1UEChMVTm9yZGVhIEJhbmsg' \
                           'QUIgKHB1YmwpMR8wHQYDVQQDExZOb3JkZWEgQ29ycG9yYXRl' \
                           'IENBIDAxMRQwEgYDVQQFEws1MTY0MDYtMDEyMDAeFw0xMzA1' \
                           'MDIxMjI2MzRaFw0xNTA1MDIxMjI2MzRaMEQxCzAJBgNVBAYT' \
                           'AkZJMSAwHgYDVQQDDBdOb3JkZWEgRGVtbyBDZXJ0aWZpY2F0' \
                           'ZTETMBEGA1UEBRMKNTc4MDg2MDIzODCBnzANBgkqhkiG9w0B' \
                           'AQEFAAOBjQAwgYkCgYEAwtFEfAtbJuGzQwwRumZkvYh2BjGY' \
                           'VsAMUeiKtOne3bZSeisfCq+TXqL1gI9LofyeAQ9I/sDm6tL8' \
                           '0yrD5iaSUqVm6A739MsmpW/iyZcVf7ms8xAN51ESUgN6akwZ' \
                           'CU9pH62ngJDj2gUsktY0fpsoVsARdrvOFk0fTSUXKWd6LbcC' \
                           'AwEAAaOCAR0wggEZMAkGA1UdEwQCMAAwEQYDVR0OBAoECEBw' \
                           '2cj7+XMAMBMGA1UdIAQMMAowCAYGKoVwRwEDMBMGA1UdIwQM' \
                           'MAqACEALddbbzwunMDcGCCsGAQUFBwEBBCswKTAnBggrBgEF' \
                           'BQcwAYYbaHR0cDovL29jc3Aubm9yZGVhLnNlL0NDQTAxMA4G' \
                           'A1UdDwEB/wQEAwIFoDCBhQYDVR0fBH4wfDB6oHigdoZ0bGRh' \
                           'cCUzQS8vbGRhcC5uYi5zZS9jbiUzRE5vcmRlYStDb3Jwb3Jh' \
                           'dGUrQ0ErMDElMkNvJTNETm9yZGVhK0JhbmsrQUIrJTI4cHVi' \
                           'bCUyOSUyQ2MlM0RTRSUzRmNlcnRpZmljYXRlcmV2b2NhdGlv' \
                           'bmxpc3QwDQYJKoZIhvcNAQEFBQADggEBACLUPB1Gmq6286/s' \
                           'ROADo7N+w3eViGJ2fuOTLMy4R0UHOznKZNsuk4zAbS2KycbZ' \
                           'sE5py4L8o+IYoaS88YHtEeckr2oqHnPpz/0Eg7wItj8Ad+AF' \
                           'tgpWRmYULtCK6jode0NhgNnAgOI9uy76pSS16aDoiQWUJqQ' \
                           'gVydowAnqS9h9aQ6gedwbOdtkWmwKMDVXU6aRz9Gvk+JeYJ' \
                           'htpuP3OPNGbbC5L7NVdno+B6AtwxmG3ozd+mPcMeVuz6kKL' \
                           'AmQyIiBSrRNa5OrTkq/CUzxO9WUgTnm/Sri7zReR6mU= '
        file_name =  'SGC_' + date + '.xml'

        secureenvelope = SecureEnvelope(customer_id, command, timestamp,
                                        environment, targetid,
                                        softwareid, filetype, content,
                                        digest_value, signature_value,
                                        x509_issuer_name, x509_serial_number,
                                        x509_certificate, file_name)
        secureenvelope.CreateXml()
        global retval
        bolag = ''  # CustomerUtil.getCurrCust(content_string)
        config = ConfigObj(os.getcwd() + '/config.ini')
        # gpghome = config['cert']['gpghome']
        # gpgbin = config['cert']['gpgbin']
        # pwd = config['cert']['password']
        # content_string =  content_string.read()

        # pygpglib = PyGpgLib(gpghome, gpgbin)
        # content_string_file = config['misc'][
        #                           'outdir'] + '/' + datetime.now().strftime(
        #     "%Y%m%d-%H%M%S") + '_noenvelope_trav.xml'
        # envelope_file = config['misc'][
        #                     'outdir'] + '/' + datetime.now().strftime(
        #     "%Y%m%d-%H%M%S") + '_trav.xml'
        # with open(content_string_file, 'w', encoding='utf8') as content:
        #     content.write(content_string)
        # envelope_file_sing = config['misc']['outdir']
        # _id = "123456"
        # date_time = datetime.fromtimestamp(time.time())
        # _date = date_time.strftime('%Y-%m-%dT%H:%M:%S%Z%z')
        # retval = pygpglib.sign_content(content_string_file, pwd,
        #                                envelope_file_sing, 'gpg')
        # # Digital sign orginal
        # log.debug(retval)
        # log.debug("signed")
        try:
            # Sending the data...
            sfthost = config['sftp2']['host']
            sftpuser = config['sftp2']['username']
            sftppw = config['sftp2']['password']
            bank_dir = config['sftp2']['bank_dir']
            envelope = config['sftp2'].as_bool('envelope')
            private_key = config['sftp2']['private_key']
            log.info("Trying to send to sftp")
            sftpclient = SftLib()
            sftpclient = sftpclient.create_sftp_client(sfthost, sftpuser, sftppw, private_key, keyfiletype)

            sftpclient.put(retval, '/' + os.path.basename(retval))

            retval = 0
        except (RuntimeError, TypeError, NameError, ValueError, IOError,
                IndexError) as err:
            log.error('EnvelopeError ..' + str(err))
        except (ConfigObjError, ConfigObjError, ConfigspecError) as Conferr:
            log.error('EnvelopeError ..' + str(Conferr))
        except SSHException as wee:
            log.error('EnvelopeError.. ' + str(wee))
        except Exception as ecj:
            log.error('EnvelopeError.. ' + str(ecj))
        finally:
            return retval
