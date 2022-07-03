#  Copyright (c) 2022. Mickael Eriksson

import paramiko
from paramiko.ssh_exception import AuthenticationException


class SftLib:
    def create_sftp_client(self, host,username, password, keyfilepath, keyfiletype):
        """
        create_sftp_client(host, port, username, password, keyfilepath, keyfiletype) -> SFTPClient

        Creates a SFTP client connected to the supplied host on the supplied port authenticating as the user with
        supplied username and supplied password or with the private key in a file with the supplied path.
        If a private key is used for authentication, the type of the keyfile needs to be specified as DSA or RSA.
        :rtype: SFTPClient object.
        """
        sftp = None
        key = None
        transport = None
        port = int('22')
        transport = paramiko.Transport((host, port))
        try:
            if len(keyfilepath):
                # Get private key used to authenticate user.
                # Create Transport object using supplied method of authentication.
                if keyfiletype == 'DSA':
                    with open(keyfilepath) as keyfile:
                    # The private key is a DSA type key.
                        key = paramiko.DSSKey.from_private_key_file(keyfile)
                        transport.connect(None, username, password,key)
                else:
                    # The private key is a RSA type key.
                    with open(keyfilepath) as keyfile:
                        key = paramiko.RSAKey.from_private_key(keyfile)
                        transport.connect(None, username, password,key)
            else:
                transport.connect(None, username, password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            return sftp
        except AuthenticationException as ea:
            print('Login error %s: %s' % (ea.__class__, ea))
        except Exception as e:
            print('An error occurred creating SFTP client: %s: %s' % (e.__class__, e))
            if sftp is not None:
                sftp.close()
            if transport is not None:
                transport.close()
            pass

    def create_sftp_client2(self, host, port, username, password, keyfilepath, keyfiletype):
        """
        create_sftp_client(host, port, username, password, keyfilepath, keyfiletype) -> SFTPClient

        Creates a SFTP client connected to the supplied host on the supplied port authenticating as the user with
        supplied username and supplied password or with the private key in a file with the supplied path.
        If a private key is used for authentication, the type of the keyfile needs to be specified as DSA or RSA.
        :rtype: SFTPClient object.
        """
        ssh = None
        sftp = None
        key = None
        try:
            if keyfilepath is not None:
                # Get private key used to authenticate user.
                if keyfiletype == 'DSA':
                    # The private key is a DSA type key.
                    key = paramiko.DSSKey.from_private_key_file(keyfilepath)
                else:
                    # The private key is a RSA type key.
                    key = paramiko.RSAKey.from_private_key(keyfilepath)

            # Connect SSH client accepting all host keys.
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password, key)

            # Using the SSH client, create a SFTP client.
            sftp = ssh.open_sftp()
            # Keep a reference to the SSH client in the SFTP client as to prevent the former from
            # being garbage collected and the connection from being closed.
            sftp.sshclient = ssh

            return sftp
        except Exception as e:
            print('An error occurred creating SFTP client: %s: %s' % (e.__class__, e))
            if sftp is not None:
                sftp.close()
            if ssh is not None:
                ssh.close()
            pass
