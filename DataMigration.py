#  -*- coding:utf-8 -*-
# by zhangxx
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='myapp.log', filemode='w')
'''
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
'''

def Log(msg):
    print msg
    logging.info(msg)

import os
import shutil
import time
from Models.UserModel import UserModel
from Models.Thing import Thing
from Models.Message import Message
from Utils.JSON import JSON
from Utils.File import File
from Utils.Time import Time
from Utils.ApiHelper import ApiHelper

if __name__ == '__main__':
    print '============ 数据迁移注意事项 ============'
    print '1.AccessKey超时是间足够长    ( 20年)'
    print '2.启用恒定失效套餐           ( 至 2015-12-31 )'
    print '3.api函数执行超时时间足够长  ( 500 秒 )'
    print '============ 数据迁移注意事项 ============'
    raw_input('按 [回车] 继续...')
    ticks = time.time()
    ecgCareOLPath = 'd:/EcgCareOL/_Store/'                              # 原数据目录
    exportPath = 'd:/ws/svn/src/trunk/Service/Api/EcgCare/raws/'        # 心电文件导出目标路径
    apiRoot = 'http://192.168.1.202:8080'                               # API 根地址
    transKey = 'NYCghQrDxkI'                                            # 传输令牌
    mgrAccount = 'zxxmgr'                                               # 主管帐号
    cusAccount = 'zxxcus'                                               # 客服帐号
    expAccount = 'zxxexp'                                               # 专家帐号
    password = '123456'                                                 # 登录密码
    schemeName = '数据迁移套餐1'                                        # 套餐名称 ( 恒定过期时间 )
    DefaultUserName = u'UnknowUser'                                     # 缺省用户名称
    DefaultUserAddr = u'未填写地址'                                     # 缺省用户地址
    # //////////////////////////////////////////////////////////
                                                                        # 检查 原数据目录是否存在
    if not os.path.exists(ecgCareOLPath): exit('[ecgCareOLPath] 目录不存在!')
    if not os.path.exists(exportPath): exit('[exportPath] 目录不存在!')# 检查 心电文件导出目标路径是否存在
    dah = ApiHelper(apiRoot, transKey)                                  # 初始化医生客户端
    cah = ApiHelper(apiRoot, transKey)                                  # 初始化客服客户端
    mah = ApiHelper(apiRoot, transKey)                                  # 初始化主管客户端
    eah = ApiHelper(apiRoot, transKey)                                  # 初始化专家客户端
    if mah.Auth(mgrAccount, password): Log(u'主管 建权成功: {0}'.format(mah.AccessKey))
    if cah.Auth(cusAccount, password): Log(u'客服 建权成功: {0}'.format(cah.AccessKey))
    if eah.Auth(expAccount, password): Log(u'专家 建权成功: {0}'.format(eah.AccessKey))
    countSucceed = 0
    schemeUnique = mah.MgrGetSchemeInfo(schemeName)['Unique']           # 获取套餐编码
    Log(u'读取EcgCareOnline平台用户列表')
    allText = File.ReadAllText(ecgCareOLPath + 'Users.json')
    jsonUsers = JSON.Deserialize(allText)
    totalUser = len(jsonUsers)
    Log(u'共需要迁移 {0} 个用户...'.format(totalUser))
    indexUser = 0
    for jsonUser in jsonUsers:
        indexUser += 1
        Log(u'正在迁移第 {0} 个用户, 共 {1} 个用户需要迁移'.format(indexUser,totalUser))
        user = JSON.DictToInst(jsonUser, UserModel())
        if 0 == len(user.userAddr):
            Log(u'!!!医生地址不得为空! 已置为缺省值.')
            user.userAddr = DefaultUserAddr
        if u'已作废' == user.userName:
            Log(u'!!!已作废 记录, 跳过, {0}'.format(user.loginName))
            continue
        if u'作废账号' == user.userName:
            Log(u'!!!已作废 记录, 跳过, {0}'.format(user.loginName))
            continue
        if u'作废' == user.userName:
            Log(u'!!!已作废 记录, 跳过, {0}'.format(user.loginName))
            continue

        Log(u'设置系统时间,统一指定医生注册时间')
        Time.setSystemTime('2015-06-30 07:00:00')
        Log(u'添加医生' + user.loginName)
        try:
            mah.AddDoc({'loginName': user.loginName, 'password': user.password, 'userName': user.userName, 'email': user.userEmail, 'docDeviceNumber': user.userDevice, 'mechanism': user.userCompany, 'docAddress': user.userAddr, 'phone': user.userPhone, 'docPostcode': user.userPostcode, 'docWechat': '', 'identityCard': '', 'gender': 0, 'faceIcon': ''})
            if dah.Auth(user.loginName, user.password): Log(u'医生 建权成功:'+dah.AccessKey)
        except Exception:
            Log(u'!!!添加医生失败 [' + user.loginName + U']')

        Log(u'获取医生信息')
        try:
            userUnique = dah.GetDocInfo()['unique']
        except Exception:
            Log(u'!!!获取医生信息失败 [' + user.loginName + U']')
            continue

        Log(u'为医生订阅套餐')
        # /api/Scheme/SchemeSubscription?accessKey=e6Kt3s13y0I&userUnique=GjgsJ7jcRE8&schemeUnique=PaJxQ4AL20M
        try:
            mah.SchemeSubscription(userUnique, schemeUnique)
        except Exception:
            Log(u'!!!订阅套餐失败 [{0}]'.format(user.loginName))
            continue

        Log(u'读取老平台测量记录...')
        UserId = user.UserId
        file = ecgCareOLPath + 'datas/' + UserId + '/things.json'
        if not os.path.exists(file):
            Log(u'!!!文件 [{0}] 不存在!'.format(file))
            continue
        Log(u'遍历测量记录')
        currUserThings = JSON.Deserialize(File.ReadAllText(file))
        countThings = len(currUserThings)
        indexThing = 0
        for jsonThing in currUserThings:
            indexThing += 1
            Log(u'正在迁移第 {0} 个用户, 共 {1} 个用户需要迁移, 当前导入第 {2} 共需要导入 {3} 条记录'.format(indexUser,totalUser, indexThing, countThings))
            thing = JSON.DictToInst(jsonThing, Thing())
            rawPath = ecgCareOLPath + 'raws/'
            if not os.path.exists(rawPath + thing.rawFile):
                Log(u'!!!raw 文件 [{0}] 不存在!'.format(thing.rawFile))
                continue

            # 更改命名规则
            # _Store/raws/FFFF0000FFFF0006.S_2015-07-10#11_03_52  >> d:/ws/svn/src/trunk/Service/Api/EcgCare/raws/09022048283729FF#2015-12-01#11_29_52_078939.etc
            # .N_ .S_ .Q_ >> #
            rawName = thing.rawFile.replace('.N_', '#').replace('.S_', '#').replace('.Q_', '#')
            rawFile = '{0}_000000.etc'.format(rawName)
            # LogPrint(rawPath + thing.rawFile + ' >> ' + exportRawPath + rawFile)
            Log(u'复制文件 [{0}]...'.format(thing.rawFile))
            shutil.copyfile(rawPath + thing.rawFile, exportPath + rawFile)
            Log(u'统计文件个数...')
            rawParts = rawName.split('#')
            rawParts.reverse()
            rawParts.pop()
            rawParts.reverse()
            rawPrefix = '#'.join(rawParts)
            countRaws = 0
            for name in os.listdir(rawPath):
                if os.path.isdir(os.path.join(rawPath, name)): continue
                if 0 == name.find(rawPrefix): countRaws += 1
            # 2015-07-10 10:31:43 => 2022015 710103143    0
            #                        2022015071010314300000
            measureTime = Time.ParseTime(thing.MeasureTime, False)
            reportCode = '202{0:4d}{1:2d}{2:2d}{3:2d}{4:2d}{5:2d}{6:5d}'.format(measureTime.year, measureTime.month, measureTime.day, measureTime.hour, measureTime.minute, measureTime.second, countRaws).replace(' ', '0')
            Log(u'根据测量记录时间设置系统时间')
            Time.setSystemTime(thing.MeasureTime)

            Log(u'添加测量记录')
            try:
                thingUnique = mah.AddThingForTest({"reportCode": reportCode, "deviceNumber": user.userDevice, "patientsName": thing.UserName, "rawFile": rawFile, "HR": thing.HR, "RR": thing.RR, "PR": thing.PR, "QT": thing.QT, "QTc": thing.QTc, "P": thing.P, "QRS": thing.QRS, "T": thing.T, "RV5": thing.RV5, "SV1": thing.SV1, "RandS": thing.RandS, "RecSeconds": thing.RecSeconds, "MeasureTime": thing.MeasureTime, })['unique']
            except Exception:
                Log(u'!!!添加测量记录操作失败! [{0}]'.format(rawFile))
                continue
            if thing.Important:
                Log(u'收藏当前测量记录')
                dah.MarkedThing(thingUnique)
            Log(u'止步于 [新记录] 状态')
            if thing.Status < 1:
                countSucceed += 1 # 统计成功导入记录数
                continue
            Log(u'设置记录为已读')
            dah.SetThingAsRead(thingUnique)
            Log(u'止步于 [已读取] 状态')
            if thing.Status < 2:
                countSucceed += 1 # 统计成功导入记录数
                continue
            Log(u'填写患者信息')
            PatientGender = 0 # female
            if thing.UserGender == 'male':
                PatientGender = 1
            if thing.UserName.strip()=='':
                Log(u'!!!患者姓名不得为空! 已置为缺省值.')
                thing.UserName = DefaultUserName
            dah.SetThingPatientInfo(thingUnique, {'PatientName': thing.UserName, 'PatientGender': PatientGender, 'PatientAge': thing.UserAge, 'Portrait': thing.Portrait, 'MedicalHistory': thing.MedicalHistory})
            Log(u'止步于 [会诊中] 状态')
            if thing.Status < 3:
                countSucceed += 1 # 统计成功导入记录数
                continue
            Log(u'发起会诊请求')
            dah.RequestDiagnosis(thingUnique)
            Log(u'接受会诊请求')
            cah.AcceptDiagnosis(thingUnique, cah.UserUnique)
            Log(u'聊天消息')

            # 遍历 Assistances.json
            # print 'uid',UserId,'tid',thing.Id # 聊天查询参数
            # raw_input('===')
            assistancesFile = ecgCareOLPath + 'datas/' + UserId + '/Assistances.json'
            if not os.path.exists(assistancesFile):
                Log('文件 [{0}] 不存在! [Enter] to continue.'.format(assistancesFile))
                continue
            for assis in JSON.Deserialize(File.ReadAllText(assistancesFile)):
                if thing.Id != assis['Id']: continue
                #print 'MessageList', len(assis['MessageList']), assis['MessageList']
                for jsonMessage in assis['MessageList']:
                    message = JSON.DictToInst(jsonMessage, Message())
                    # print 'time:', message.time, 'owner:', message.owner, 'ownerType:', message.ownerType, 'message:', message.message, 'readed:', message.readed
                    # raw_input('******')
                    if message.ownerType < 1: continue
                    if message.message == u'您好, 已给出会诊建议, 请刷新报告查看结果.':continue
                    if message.ownerType == 1:
                        cah.SendMessage(thingUnique, message.message)
                    if message.ownerType == 2:
                        dah.SendMessage(thingUnique, message.message)

            Log(u'填写诊断结论')
            cah.EditDiagnosisConclusion(thingUnique, eah.UserUnique, thing.Analysis, thing.Conclusion)
            Log(u'止步于 [已诊断] 状态')
            if thing.Status < 4:
                countSucceed += 1 # 统计成功导入记录数
                continue
            Log(u'关闭会诊')
            dah.CloseDiagnosis(thingUnique)
            countSucceed += 1   # 统计成功导入记录数
    Log(u'使用 NTP 网络授时服务将时间同步至北京时间')
    Time.syncNTPTime()
    time.sleep(2)
    ticks = time.time() - ticks # 计算时间消耗
    Log(u'共成功迁移 {0} 条记录, 耗时: {1} 秒'.format(countSucceed, ticks))










