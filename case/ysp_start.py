# -*- coding: utf-8 -*- 
"""Created by ssfanli on 2022/03/03 
"""
from utils.const import PLATFORM,  PACKAGE, COMMON
from utils.install import Installer
from utils.uidriver import BaseOperateAND, BaseOperateIOS


class YSPStart(object):

    def __init__(self, platform: str, device_id: str):
        self.plat = platform
        self.did = device_id
        self.pkg_name = PACKAGE.YSP_AND if self.plat == PLATFORM.AND else PACKAGE.YSP_IOS
        self.bo = None

    @property
    def boss_divide_id(self):
        """get divide id

        ios need install and init firstly
        """
        if self.plat == PLATFORM.AND:
            return COMMON.divide_id_mapping[self.did]
        if not self.bo:
            self.app_init()
        return self.bo.get_idfv()

    def download(self, which, version):
        raise NotImplementedError

    def install(self, app_path):
        ins = Installer(self.plat, self.did)
        ins.install(app_path, self.pkg_name)

    def app_init(self):
        if self.plat == PLATFORM.AND:
            self.bo = BaseOperateAND(self.did, self.pkg_name)
        else:
            self.bo = BaseOperateIOS(self.did, self.pkg_name)

    def external_start(self):
        raise NotImplementedError

    def cold_start(self):



        def start():
            pass
        pass
