#  -*- coding:utf-8 -*-
# by zhangxx
import socket

import datetime
import struct
import time
import win32api

class Time:
    @classmethod
    def syncNTPTime(self):
        TIME_1970 = 2208988800L
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = '\x1b' + 47 * '\0'
        TimeServer = '210.72.145.44'    # 国家授时中心ip
        TimeServer = 's1b.time.edu.cn'  # 清华大学
        TimeServer = 's2c.time.edu.cn'  # 北京邮电大学
        Port = 123
        client.sendto(data, (TimeServer, Port))
        data, address = client.recvfrom(1024)
        data_result = struct.unpack('!12I', data)[10]
        data_result -= TIME_1970
        tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(data_result)
        win32api.SetSystemTime(tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, 0)

    @classmethod
    def ParseTime(self, str, gmt=True):
        # dt = "2015-07-10 10:31:43"
        st = time.strptime(str, "%Y-%m-%d %H:%M:%S")
        dt = datetime.datetime(st.tm_year, st.tm_mon, st.tm_mday, st.tm_hour, st.tm_min, st.tm_sec)
        if gmt:
            return dt + datetime.timedelta(hours=-8)
        return dt + datetime.timedelta(hours=-0)

    @classmethod
    def setSystemTime(self, str):
        t = self.ParseTime(str)
        win32api.SetSystemTime(t.year, t.month, 0, t.day, t.hour, t.minute, t.second, 0)

'''
if __name__ == '__main__':
    Time.setSystemTime('2008-12-23 13:14:15')
'''