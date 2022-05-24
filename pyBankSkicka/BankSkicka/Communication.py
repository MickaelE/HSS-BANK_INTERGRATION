#  Copyright (c) 2021-2022. Mickael Eriksson

import pysftp
from pysftp.exceptions import ConnectionException, CredentialException, HostKeysException

from global_logger import Log

log = Log.get_logger(logs_dir='logs')


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


class Communication:

    def __init__(self, host, username, password, bank_dir, private_key):

        # Instance Variable
        self.host = host
        self.username = username
        self.password = password
        self.bank_dir = bank_dir
        self.private_key = private_key

    def __send__(self, file):
        """
        Send xml file to the bank's sftp server.
        :param file: The file to be sent.
        :return:
        """
        try:
            log.info("SFTP: Trying to connect.")
            if self.private_key is not None:
                with pysftp.Connection(self.host, username=self.username, private_key=self.private_key) as sftp:
                    with sftp.cd(self.bank_dir):
                        sftp.put(file)
            else:
                with pysftp.Connection(self.host, username=self.username, password=self.password) as sftp:
                    with sftp.cd(self.bank_dir):
                        sftp.put(file)

            log.info("SFTP: Success sending")
        except (ConnectionException, CredentialException, HostKeysException, FileNotFoundError, IOError) as e:
            log.error("SFTP: " + str(e))
        except Exception as ex:
            log.error('SFTP: ' + str(ex))
        finally:
            pysftp.Connection.close

    def __receive__(self, file):
        """
            Fetches file from sftp server.
            :param file: File to fetch
            :return:
            """
        try:
            with pysftp.Connection(self.host, self.username, self.password) as sftp:
                with sftp.cd(self.bank_dir):
                    sftp.get(file, preserve_mtime=True)
                    sftp.get('remote_file')
        except (ConnectionException, CredentialException, HostKeysException) as e:
            log.error(e)
