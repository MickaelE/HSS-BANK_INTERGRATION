import os
from unittest import TestCase

import sftpserver as sftpserver
from configobj import ConfigObj
from contextlib import closing
import py.path
from pyBankSkicka.BankSkicka.ftpClient import SftLib


class TestSftpClient(TestCase):
    def setUp(self):
        self.sftLib = SftLib()


class Test(TestSftpClient):
    def test_sftp_client_put(self, retval=None):
        confile = os.getcwd() + '/config.ini'
        config = ConfigObj(confile)
        sfthost = config['sftp1']['host']
        sftpuser = config['sftp1']['username']
        sftppw = config['sftp1']['password']
        bank_dir = config['sftp1']['bank_dir']
        envelope = config['sftp1'].as_bool('envelope')
        private_key = config['sftp1']['private_key']
        sftpclient = self.sftLib.create_sftp_client(sfthost,sftpuser,
                                                    sftppw, private_key, 'RSA')
        localpath = "/home/xmie/test_trav.gpg"
        filepath = "/sftpuser/test_trav.gpg"
        assert(sftpclient.put(localpath,filepath))

    def test_sftp_client_get(self, retval=None):
        confile = os.getcwd() + '/config.ini'
        config = ConfigObj(confile)
        sfthost = config['sftp1']['host']
        sftpuser = config['sftp1']['username']
        sftppw = config['sftp1']['password']
        bank_dir = config['sftp1']['bank_dir']
        envelope = config['sftp1'].as_bool('envelope')
        private_key = ''  # config['sftp1']['private_key']
        sftpclient = self.sftLib.create_sftp_client(sfthost, sftpuser,
                                                    sftppw, private_key, 'RSA')
        localpath = "/home/xmie/test_trav.gpg"
        filepath = "/sftpuser/test_trav.gpg"
        assert (sftpclient.get(filepath,localpath))


