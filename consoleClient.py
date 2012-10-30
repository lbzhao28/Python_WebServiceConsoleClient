__author__ = 'stone'
#coding=UTF-8
import traceback
from configData import getConfig
from logHelper import getLogger
import pycurl
import cStringIO
import json
import DbModule

from apscheduler.scheduler import Scheduler

from soapClient import deliverySend

#def job_function(text):
#    print text

#from datetime import datetime

#job = sched.add_date_job(job_function,datetime(2012,9,20,18,22,00),['Hello World'])

#sched.start()

sched = Scheduler()
sched.daemonic = False
sched.start()

def getOrderTrans(inOrderid):
    try:
        buf = cStringIO.StringIO() #define in function.
        c = pycurl.Curl()
        localURL = getConfig('RESTService','transUrl','str')+inOrderid
        localURL = str(localURL)
        c.setopt(pycurl.URL,localURL)
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.USERPWD,getConfig('allowedUser1','UserName','str')+':'+getConfig('allowedUser1','Password','str'))
        c.perform()

        #get the data from json.
        localOrderInfo = json.loads(buf.getvalue())
        buf.close()

        return localOrderInfo

    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

def job_function():
    try:
        logger = getLogger()
        logger.debug("start job function")

        logger.debug("start get mailid")
        lstOrderid = DbModule.getData4DbSqlite()

        for strOrderid in lstOrderid:
            strHeaderIndex = strOrderid.find('GWImp')
            strOrderidSearch = strOrderid
            # first got it.
            if (strHeaderIndex == 0):
                strOrderidSearch = strOrderid[len('GWImp'):len(strOrderid)]
            orderTransInfos = getOrderTrans(strOrderidSearch)

            strMailid = orderTransInfos['mailid']
            strCompanytile = orderTransInfos['companytitle']

            if (strMailid is not None) & (strMailid != "") & (strCompanytile is not None) & (strCompanytile != ""):
                logger.debug("start callwebservice")
                returnStatus = deliverySend(strOrderidSearch,strCompanytile,strMailid)
                #if return success,delete the record.
                if (returnStatus == '5'):
                    logger.debug("delete record")
                    DbModule.delData4DbSqlite(strOrderid)

                pass
    except :
        logger.error("exception occur, see the traceback.log")
        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()
    else:
        pass
    finally:
        pass

sched.add_interval_job(job_function, seconds = getConfig('freqTimer','freqSecond','int') ,start_date= getConfig('freqTimer','starttime','str'))
sched.start()

#def job_function():
#    print "Hello World"

#sched.add_interval_job(job_function, minutes=1, start_date='2012-09-20 18:00:00')
#sched.add_interval_job(job_function, seconds=5, start_date='2012-09-20 18:00:00')
#sched.start()


#@sched.interval_schedule(seconds=5, start_date='2012-04-12 09:54:59')
#def job_function():
#    print "Hello World"

