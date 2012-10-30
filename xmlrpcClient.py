__author__ = 'stone'
#coding=UTF-8
import xmlrpclib
from xmlrpclib import *

def apiserver(address):
    """connect to server return server object"""
    return xmlrpclib.Server(address)
    pass

def apisession(server, username, password):
    """open an api session and return the string"""
    return server.login(username, password)
    pass

server = apiserver('http://www.cobor.cn/api/xmlrpc')
session = apisession(server,'dirk', 'dirk123')

def deliverySend(server,session):
    """send the mail id using the api"""
    # retrieve current set information
    # build the dict for the mail id.
    data = dict({
        'user':'dirk',
        'pass':'dirk123',
        'order_id':'100000213',
        'title':'圆通快递',
        'track_id':'10000042',
    })

    return server.call(session,'sales_order_shipment.deliverySend',data)

if __name__ == "__main__":
    deliverySend(server,session)
    #server = Server('http://www.cobor.cn/api/xmlrpc')
    #session = server.login('user','password')
    pass

