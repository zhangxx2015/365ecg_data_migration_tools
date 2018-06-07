#  -*- coding:utf-8 -*-
# by zhangxx

import sys
import urllib
import urllib2
import json

from Models.Resp import Resp
from Utils.JSON import JSON


class ApiHelper:
    ApiRoot = ''
    TransServiceAccessKey = ''
    AccessKey = ''
    UserUnique = ''

    def __init__(self, apiRoot, transServiceAccessKey):
        self.ApiRoot = apiRoot
        self.TransServiceAccessKey = transServiceAccessKey

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
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Auth', {
            'loginName': loginName,
            'password': password
        })), Resp())
        if resp.Status != 'OK':
            print resp.Error
            raise Exception(resp.Error)
        self.AccessKey = resp.data["accessKey"]
        self.UserUnique = resp.data["userUnique"]
        return True

    def AddDoc(self, args):
        '''
        print args
        xbody = self.http_post(self.ApiRoot + '/api/Doctor/AddDoc?accessKey='+self.AccessKey, args)
        print 'xbody:', xbody
        raw_input('...')
        resp = JSON.DictToInst(json.loads(xbody),Resp())
        '''
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Doctor/AddDoc?accessKey=' + self.AccessKey, args)), Resp())
        if resp.Status != 'OK':
            print args
            print resp.Error
            raise Exception(resp.Error)
        return True

    def GetDocInfo(self):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Doctor/GetDocInfo?accessKey={0}'.format(self.AccessKey), {})), Resp())
        if resp.Status != 'OK':
            print resp.Error
            raise Exception(resp.Error)
        if len(resp.data) < 1:
            print resp.Error
            raise Exception(resp.Error)
        return resp.data[0]

    def MgrGetSchemeInfo(self, schemeName):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Scheme/MgrGetSchemeList?accessKey={0}'.format(self.AccessKey), {
            'pageIndex': 0,
            'pageSize': 1,
            'SchemeCode': schemeName,
            'SchemeEnabled': 1,
            'SchemeType': -1,
            'PerCharge': '',
            'CreateDateFrom': '',
            'CreateDateDateTo': ''
        })), Resp())
        if resp.Status != 'OK':
            print resp.Error
            raise Exception(resp.Error)
        if len(resp.data) < 1:
            print resp.Error
            raise Exception(resp.Error)
        return resp.data[0]

    def SchemeSubscription(self, userUnique, schemeUnique):
        # /api/Scheme/SchemeSubscription?accessKey=e6Kt3s13y0I&userUnique=GjgsJ7jcRE8&schemeUnique=PaJxQ4AL20M
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Scheme/SchemeSubscription?accessKey={0}&userUnique={1}&schemeUnique={2}'.format(self.AccessKey, userUnique, schemeUnique), {})), Resp())
        if resp.Status != 'OK':
            print 'userUnique:', userUnique
            print 'schemeUnique:', schemeUnique
            print resp.Error
            raise Exception(resp.Error)
        return True


    def AddThingForTest(self, args):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Thing/AddThingForTest?transServiceAccessKey=' + self.TransServiceAccessKey, args)), Resp())
        if resp.Status != 'OK':
            print args
            print resp.Error
            raise Exception(resp.Error)
        if len(resp.data) < 1:
            print resp.Error
            raise Exception(resp.Error)
        return resp.data

    def MarkedThing(self, jsonThingUniqueList):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Thing/MarkedThing?accessKey=' + self.AccessKey + '&jsonThingUniqueList=' + jsonThingUniqueList, {})), Resp())
        if resp.Status != 'OK':
            print jsonThingUniqueList
            print resp.Error
            raise Exception(resp.Error)
        return True

    def SetThingAsRead(self, thingUnique):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Thing/SetThingAsRead?accessKey=' + self.AccessKey + '&thingUnique=' + thingUnique, {})), Resp())
        if resp.Status != 'OK':
            print thingUnique
            print resp.Error
            raise Exception(resp.Error)
        return True

    def SetThingPatientInfo(self, thingUnique, args):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Thing/SetThingPatientInfo?accessKey=' + self.AccessKey + '&thingUnique=' + thingUnique, args)), Resp())
        if resp.Status != 'OK':
            print args
            print resp.Error
            raise Exception(resp.Error)
        return True

    def RequestDiagnosis(self, thingUnique):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Diagnosis/RequestDiagnosis?accessKey=' + self.AccessKey + '&thingUnique=' + thingUnique, {})), Resp())
        if resp.Status != 'OK':
            print thingUnique
            print resp.Error
            raise Exception(resp.Error)
        return True


    def AcceptDiagnosis(self, thingUnique, curUnique):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Diagnosis/AcceptDiagnosis?accessKey=' + self.AccessKey + '&thingUnique=' + thingUnique + '&curUnique=' + curUnique, {})), Resp())
        if resp.Status != 'OK':
            print thingUnique
            print resp.Error
            raise Exception(resp.Error)
        return True



    def EditDiagnosisConclusion(self, thingUnique, expertUnique, expertDiagnosis, expertAdvice):
        url = self.ApiRoot + '/api/Diagnosis/EditDiagnosisConclusion?accessKey=' + self.AccessKey + '&thingUnique=' + thingUnique + '&expertUnique=' + expertUnique + '&expertDiagnosis=' + urllib.quote(expertDiagnosis.encode('utf8')) + '&expertAdvice=' + urllib.quote(expertAdvice.encode('utf8'))
        resp = JSON.DictToInst(json.loads(self.http_post(url, {})), Resp())
        if resp.Status != 'OK':
            print thingUnique
            print resp.Error
            raise Exception(resp.Error)
        return True


    def CloseDiagnosis(self, thingUnique):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Diagnosis/CloseDiagnosis?accessKey=' + self.AccessKey + '&thingUnique=' + thingUnique, {})), Resp())
        if resp.Status != 'OK':
            print thingUnique
            print resp.Error
            raise Exception(resp.Error)
        return True

    def SendMessage(self, thingUnique, content):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/IM/SendMessage?accessKey=' + self.AccessKey, {
          'thingUnique': thingUnique,
          'from': '',
          'to': '',
          'content': content,
          'msgType': 0
        })), Resp())
        if resp.Status != 'OK':
            print thingUnique
            print resp.Error
            raise Exception(resp.Error)
        return True

    def DocGetThingList(self, args):
        resp = JSON.DictToInst(json.loads(self.http_post(self.ApiRoot + '/api/Thing/DocGetThingList?accessKey=' + self.AccessKey, args)), Resp())
        if resp.Status != 'OK':
            print args
            print resp.Error
            raise Exception(resp.Error)
        return resp
