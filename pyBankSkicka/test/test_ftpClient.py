import os
from unittest import TestCase
from configobj import ConfigObj

from pyBankSkicka.BankSkicka.ftpClient import sftLib


class TestSftpClient(TestCase):
    def setUp(self):
        self.sftLib = sftLib()


class Test(TestSftpClient):
    def test_create_sftp_client(self, retval=None):
        confile = os.getcwd() + '/config.ini'
        config = ConfigObj(confile)
        sfthost = config['sftp1']['host']
        sftpuser = config['sftp1']['username']
        sftppw = config['sftp1']['password']
        bank_dir = config['sftp1']['bank_dir']
        envelope = config['sftp1'].as_bool('envelope')
        private_key = config['sftp1']['private_key']
        sftpclient = self.sftLib.create_sftp_client(sfthost, sftpuser,
                                                    sftppw, bank_dir,
                                                    private_key, 'RSA')
        sftpclient.send(retval)
        assert False
