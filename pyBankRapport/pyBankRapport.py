#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import sys

from configobj import ConfigObj

from bankfiler.InputClass import InputsClass
from bankfiler.__init__ import main

config = ConfigObj(os.getcwd() + '/config.ini')
if __name__ == '__main__':
    if len(sys.argv) == 2:
        files = str(sys.argv[1])
        InputsClass.parsecam54(files)
    else:
        main()
        #file_destination="/data/oradir/TSPORT/sport/ekonomi"
        #shutil.move(files, file_destination)