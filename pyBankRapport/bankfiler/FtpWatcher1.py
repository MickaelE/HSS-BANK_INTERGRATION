#!/usr/bin/env python3
# -*- coding: utf-8 -*- L
# ----------------------------------------------------------------------------
# Created By  : Mickael Eriksson
# Created Date: 20220421
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Module that checks bank ftp regulary for files..
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from paramiko.ssh_exception import AuthenticationException, BadHostKeyException, ChannelException, ConfigParseError \
    , CouldNotCanonicalize

from bankfiler.Camt54c import FileFormatParser
from MickeNet.PyGPGlib import PyGpgLib
import paramiko
from global_logger import Log
from bankfiler.Camt54d import InputsClass

log = Log.get_logger(logs_dir='logs')


class FtpWatcher:
    def __init__(self, host, username, password, bank_dir, localfile, filepattern, private_key, gpghome, gpgbin):
        # Instance Variable
        self.sftp = paramiko.SSHClient()
        self.sftp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.host = host
        self.username = username
        self.password = password
        self.bank_dir = bank_dir
        self.localfile = localfile
        self.filepattern = filepattern
        self.private_key = private_key
        self.pyGpgLib = PyGpgLib(gpghome, gpgbin)

    def action(self, xmlfile):
        remote_file_path = xmlfile
        local_file_path = self.localfile + xmlfile

        try:
            client = self.sftp.open_sftp()
            client.get(remote_file_path, local_file_path)

        except (AuthenticationException, BadHostKeyException, ChannelException, ConfigParseError, CouldNotCanonicalize) \
                as e:
            log.error("SFTP Error: " + str(e))
        except Exception as e:
            log.error("SFTP Error: " + str(e))
        finally:
            # Digital sign.sign
            with open(local_file_path, 'r') as env:
                f = env.read()
            envelope_string = f
            envelope_file_sing = local_file_path + '.xml'

            textfile = open(envelope_file_sing, "w")
            a = textfile.write(str(envelope_string))
            textfile.close()
            new_path = self.pyGpgLib.verify_content(local_file_path, 'T3a4ever@', self.localfile)
            if '54D' in local_file_path:
                InputsClass.ParseDebitorFile(new_path)
            else:
                FileFormatParser.ParseCreditorFile(new_path)

    def watch(self):
        try:

            if self.private_key is not None:
                self.sftp.connect(self.host, username=self.username, key_filename=self.private_key, timeout=10.0)
            else:
                self.sftp.connect(self.host, username=self.username, password=self.password, timeout=10.0)
            #  directory_structure = self.sftp.listdir_attr(self.bank_dir)
            self.sftp = self.sftp.open_sftp()
            for f in sorted(self.sftp.listdir_attr(self.bank_dir), key=lambda k: k.st_mtime, reverse=True):

                if '54D' in f.filename:
                    self.action(f.filename)
                else:
                    log.info("No 54D")

        except (AuthenticationException, BadHostKeyException, ChannelException, ConfigParseError, CouldNotCanonicalize) \
                as e:
            log.error("SFTP Error: " + str(e))
        except Exception as ex:
            log.error('Error: ' + str(ex))
