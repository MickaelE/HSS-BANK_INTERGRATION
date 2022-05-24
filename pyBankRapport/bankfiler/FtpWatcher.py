import MickeNet
import pysftp
from MickeNet.PyGPGlib import PyGpgLib
from pysftp.exceptions import ConnectionException, CredentialException, HostKeysException
from global_logger import Log
from bankfiler.InputClass import InputsClass
log = Log.get_logger(logs_dir='logs')


class FtpWatcher:
    def __init__(self, host, username, password, bank_dir, localfile, filepattern, private_key, gpghome, gpgbin):
        # Instance Variable
        self.sftp = None
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
            with self.sftp.cd(self.bank_dir):
                print(self.sftp.getcwd() + ' ' + local_file_path)

                self.sftp.get(remote_file_path, local_file_path)
                # self.sftp.remove(remote_file_path)

        except (ConnectionException, CredentialException, HostKeysException, FileNotFoundError) as e:
            log.error(e)
        except Exception as e:
            log.error(e)
        finally:
            self.sftp.close()
            # Digital sign.sign
            with open(local_file_path, 'r') as env:
                f = env.read().encode('utf-8').strip()
            envelope_string = f
            envelope_file_sing = local_file_path + '.xml'

            textfile = open(envelope_file_sing, "w")
            a = textfile.write(str(envelope_string))
            textfile.close()
            new_path = self.pyGpgLib.verify_content(envelope_file_sing,'T3a4ever@',local_file_path)
            InputsClass.parsecam54(new_path)

    def watch(self):
        try:
            if self.private_key is not None:
                self.sftp = pysftp.Connection(host=self.host, username=self.username, private_key=self.private_key)
            else:
                self.sftp = pysftp.Connection(host=self.host, username=self.username, password=self.password)
            #  directory_structure = self.sftp.listdir_attr(self.bank_dir)
            for f in sorted(self.sftp.listdir_attr(self.bank_dir), key=lambda k: k.st_mtime, reverse=True):
                if f.filename.find('54D'):
                    self.action(f.filename)
                else:
                    log.info("No 54D")

        except (ConnectionException, CredentialException, HostKeysException) as e:
            log.error(e)
        except Exception as ex:
            log.error('Error: ' + str(ex))
