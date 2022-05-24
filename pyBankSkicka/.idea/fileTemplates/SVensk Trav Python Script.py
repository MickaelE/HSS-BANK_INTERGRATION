#!/usr/bin/env python
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
# Generic/Built-in
import datetime
import argparse
# Other Libs
import logging
import databaseconfig as cfg

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG)
# {code}