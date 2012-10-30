__author__ = 'stone'
#coding=UTF-8
import web
import traceback
from configData import getConfig
from logHelper import getLogger

def DbConnect():
    db = web.database(dbn=getConfig('db','dbname','str'),db=getConfig('db','dbservice','str'),user=getConfig('db','dbuser','str'),pw=getConfig('db','dbpwd','str'))
    return db

def DbSqliteConnect():
    db = web.database(dbn=getConfig('dbSqlite','dbname','str'),db=getConfig('dbSqlite','dbfile','str'))
    return db

def getData4DbSqlite():
    try:
        logger = getLogger()
        logger.debug("start getData4DbSqlite")
        retList = list()
        dbSqlite = DbSqliteConnect()
        entries = dbSqlite.select('orderHist',what='orderid')
        for val in entries:
            localOrderid = val.orderid
            retList.append(localOrderid)

        if (len(retList)>0):
            return retList

    except :
        logger.error("exception occur, see the traceback.log")
        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()
        ret = False
    else:
        pass
    finally:
        pass

def delData4DbSqlite(inOrderid):
    try:
        logger = getLogger()
        logger.debug("start delData4DbSqlite")
        ret = True
        dbSqlite = DbSqliteConnect()
        ret = dbSqlite.delete('orderHist',where='orderid = $delOrderid',vars={'delOrderid':inOrderid})
    except :
        logger.error("exception occur, see the traceback.log")
        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()
        ret = False
    else:
        pass
    finally:
        return ret
        pass
