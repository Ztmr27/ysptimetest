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
