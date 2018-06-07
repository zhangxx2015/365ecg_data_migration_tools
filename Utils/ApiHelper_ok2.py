#  -*- coding:utf-8 -*-
# by zhangxx

import urllib2
import json

from Models.Resp import Resp
from Utils.JSON import JSON

class ApiHelper:
    ApiRoot = ''
    AccessKey = ''

    def __init__(self, apiRoot):
        self.ApiRoot = apiRoot

    def http_post(self, url, params):
        return urllib2.urlopen(urllib2.Request(
            url, # 请求地址
            json.dumps(params), # 请求参数
            {# HTTP headers
             'Content-Type': 'application/json',
             'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
             'Cache-Control': 'no-cache'
            })).read().decode('UTF-8')

    def Auth(self, loginName, password):
        dict = json.loads(self.http_post(self.ApiRoot + '/api/Auth', {
            'loginName': loginName,
            'password': password
        }))

        resp = JSON.DictToInst(dict,Resp())

        #resp = Resp()
        #for k, v in dict.iteritems():
        #    setattr(resp, k, v)

        '''
        print 'total    :', resp.total
        print 'PageMax  :', resp.PageMax
        print 'pageIndex:', resp.pageIndex
        print 'pageSize :', resp.pageSize
        print 'Request  :', resp.Request
        print 'Status   :', resp.Status
        print 'ResType  :', resp.ResType
        print 'Error    :', resp.Error
        print 'data     :', resp.data
        '''
        print 'Status',resp.Status
        raw_input('any key to continue')


        if resp.Status != 'OK':
            print resp.Error
            raise Exception(resp.Error)
        self.AccessKey = resp.data["accessKey"]
        return True

    def AddDoc(self,args):
        dict = json.loads(self.http_post(self.ApiRoot + '/api/Doctor/AddDoc', args))
