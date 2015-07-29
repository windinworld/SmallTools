#!/usr/bin/env python

from ConfigParser import ConfigParser
from pprint import pprint
import logging
import os,sys
import commands
import MySQLdb
import logging
import logging.handlers

CONFFILE = "db.cfg"
LOGFILE = 'check_db.log'
handler = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('check_db')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.info('Begin check message ===============================================================')


def parser_config(CONFFILE):
    '''
    Parser the config file , then return a dict array
    '''
    config = ConfigParser()
    config.read(CONFFILE)
    db_info = {}
    sections = config.sections()
    for section in sections:
        db_info[section] = {}
        db_info[section]['db_host_name'] = config.get(section,'db_host_name')
        db_info[section]['user'] = config.get(section,'user')
        db_info[section]['password'] = config.get(section,'password')
        db_info[section]['databases'] = config.get(section,'databases').split(',')
    return db_info

def check_db_avail(db_info):
    '''
    check mysql connectivity according to configuration
    '''
    for section in db_info.iterkeys():
        for database in db_info[section]['databases']:
        #    print database
            #ret = os.popen("ls -l").read()
            user = db_info[section]['user']
            pw = db_info[section]['password']
            host = db_info[section]['db_host_name']
            (status,output) = commands.getstatusoutput("mysql --connect_timeout=5 -u%s -p%s -h%s %s -e 'status' 2>&1 1>/dev/null" % (user,pw,host,database))
            if 'status' not in db_info[section] : db_info[section]['status'] = {}
            db_info[section]['status'][database] = status
         #   print "Host",host ,status,output
            logger.info("HOST: %s, DB: %s, STATUS: %s, OUTPUT: %s" %(host,database,status,output))
def report_status(db_info):
    '''
    report result according to check return status
    '''
    flag = True
    count = 0
    for section in db_info.iterkeys():
        for database in db_info[section]['status'].iterkeys():
             if db_info[section]['status'][database] != 0:
                flag = False
        #       print "host: %s database: %s status: %s" %(db_info[section]['db_host_name'],database,db_info[section]['status'][database])
                count+=1
        #       count = 5
                logger.info("[ERROR] HOST: %s DB: %s STATUS: %s" %(db_info[section]['db_host_name'],database,db_info[section]['status'][database]))
    if flag:
        #print "all ok"
        sys.exit(0)
    else:
        #print "error %d" % count
        sys.exit(count)


db_info = parser_config(CONFFILE)
check_db_avail(db_info)
report_status(db_info)
#pprint(db_info)
