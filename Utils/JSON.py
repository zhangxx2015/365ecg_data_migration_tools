#  -*- coding:utf-8 -*-
# by zhangxx
import json

class JSON:
    @classmethod
    def DictToInst(self,dicts,inst):
        for k, v in dicts.iteritems():
            setattr(inst, k, v)
        return inst

    @classmethod
    def Deserialize(self,text):
        return json.loads(text)