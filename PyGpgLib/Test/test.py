#!/usr/bin/env python3

from MickeNet.PyGPGlib import PyGpgLib
path = '/opt/app/bankapp/files/camt054D_1020612860.xml'
pygpglib = PyGpgLib('/home/oracle/.gnupg', '/usr/bin/gpg')
ps = pygpglib.verify_content(path, 'T3a4ever@', '/opt/app/bankapp/files/', 'xml')
print(ps)
