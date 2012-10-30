__author__ = 'stone'
#coding=UTF-8
import traceback
from configData import getConfig
from logHelper import getLogger
import json

from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

def deliverySend(orderid,title,mailid):
    try:
        logger = getLogger()
        logger.debug("start deliverySend")
        """send the mail id using the api"""
        # build the dict for the mail id.
        data = dict({
            'user':getConfig('soapWebservice','UserName','str'),
            'pass':getConfig('soapWebservice','Password','str'),
            'order_id':orderid,
            'title':title,
            'track_id':mailid,
            })
        jsonData = json.dumps(data)
        url = getConfig('soapWebservice','url','str')
        #无法直接连接，因为不同的soap标准，所以要加上配置参数
        #c = Client(url)
        c = Client(url,doctor=ImportDoctor(Import(getConfig('soapWebservice','soapencoding','str'))))
        sid = c.service.login(getConfig('soapWebservice','UserName','str'), getConfig('soapWebservice','Password','str'))
        #result = c.service.sales_order_shipment.deliverySend(data)
        result = c.service.call(sid,getConfig('soapWebservice','serviceName','str'),jsonData)

        jsonResults = json.loads(result)
        returnStatus = jsonResults['status']

        logger.debug('returnStatus is :'+returnStatus)

        if (returnStatus == '5'):
            logger.debug('deliverySend success')
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
        return returnStatus



    #return server.call(session,'sales_order_shipment.deliverySend',data)

if __name__ == "__main__":
    deliverySend()

