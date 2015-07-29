#!/usr/bin/env python

from ConfigParser import ConfigParser
CONFIGFILE =  "stocks.cfg"

config = ConfigParser()
config.read(CONFIGFILE)

print config.get('messages','greeting')

