#  -*- coding:utf-8 -*-
# by zhangxx

import os

class File:
    @classmethod
    def ReadAllText(self,file):
        if os.path.exists(file):
            if os.path.isfile(file):
                f = open(file, 'r')
                allTexts = f.read()
                f.close()
                return allTexts.decode('UTF-8')
