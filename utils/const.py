# -*- coding: utf-8 -*- 
"""Created by ssfanli on 2022/03/02 
"""
from enum import Enum


class PLATFORM(str, Enum):
    IOS = 'ios'
    AND = 'android'


class PACKAGE(str, Enum):
    YSP_IOS = 'com.cctv.yangshipin.app.iphone'
    YSP_AND = 'com.cctv.yangshipin.app.androidp'


class COMMON:
    divide_id_mapping = {
        'TEV0217315000851': '864682039607148',  # mate9pro
        'UMX0220C23004116': '6a646c25d5b51854',  # nova 7
        'XPL0219C18016526': '',  # mate 30
        'TTNGK21603000006': '',  # honor 30 pro+
        '5EF0217B22004759': '862005033754918',  # mate 9
        '9cc46ae4': '4781d134675f6f6d',  # OPPO k9
    }
