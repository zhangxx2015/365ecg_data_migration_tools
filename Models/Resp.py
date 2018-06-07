#  -*- coding:utf-8 -*-
# by zhangxx

class Resp:
    #定义基本属性
    total = 0    # 记录总数
    PageMax = 0    # 分页上限
    pageIndex = 1    # 分页索引
    pageSize = 20    # 分页大小
    Request = ''    # 请求内容
    Status = ''    # 返回状态
    ResType = ''    # 返回内容
    Error = ''    # 错误
    data = {}    # 数据
    #定义私有属性,私有属性在类外部无法直接进行访问
    #__weight = 0
    #定义构造方法
    def __init__(self):
        self.total = 0    # 记录总数
        self.PageMax = 1    # 分页上限
        self.pageIndex = 1    # 分页索引
        self.pageSize = 20    # 分页大小
        self.Request = ''    # 请求内容
        self.Status = ''    # 返回状态
        self.ResType = ''    # 返回内容
        self.Error = ''    # 错误
        self.data = {}    # 数据