#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from configobj import ConfigObj
from bankfiler.Camt54c import FileFormatParser
from bankfiler.Camt54d import InputsClass
from bankfiler.__init__ import main

config = ConfigObj(os.getcwd() + '/config.ini')
if __name__ == '__main__':
    if len(sys.argv) == 3:
        files = str(sys.argv[1])
        if str(sys.argv[2]) == '54d':
            InputsClass.ParseDebitorFile(files)
        else:
            FileFormatParser.ParseCreditorFile(files)
    else:
        main()
