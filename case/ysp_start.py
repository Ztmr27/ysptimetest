# -*- coding: utf-8 -*- 
"""Created by ssfanli on 2022/03/03 
"""


class BaseProcess(object):

    def __init__(self, platform: str):
        pass

    def download(self, which, version):
        raise NotImplementedError

    def install(self, ):
        pass

    def cold_start(self):
        pass

    def external_start(self):
        pass