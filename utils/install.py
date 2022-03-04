# -*- coding: utf-8 -*- 
"""Created by ssfanli on 2022/03/02 
"""
import os
import re

from loguru import logger

from utils.const import *


class Installer(object):

    def __init__(self, platform: str, device_id: str):
        assert platform in (PLATFORM.AND, PLATFORM.IOS), f'platform should in (ios, android)'
        self.plat = platform
        self.did = device_id

    @staticmethod
    def _exec(cmd):
        with os.popen(cmd) as po:
            return po.readlines()

    def _is_install(self, package_name):

        def _app_list(device_id) -> list:
            if self.plat == PLATFORM.AND:
                cmd = f'adb -s {device_id} shell pm list packages'
            else:
                cmd = f'tidevice -u {device_id} applist'
            return self._exec(cmd)

        app_list = _app_list(self.did)
        if app_list:
            res = [x for x in app_list if package_name in x]
            if res:
                logger.debug(f'app: {package_name}, installed')
                return True
            else:
                logger.debug(f'app: {package_name}, not installed')
                return False
        logger.warning(f'app_list is empty')
        return False

    def _uninstall(self, package_name):
        if self._is_install(package_name):
            if self.plat == PLATFORM.AND:
                cmd = f'adb -s {self.did} uninstall {package_name}'
            else:
                cmd = f'tidevice -u {self.did} uninstall {package_name}'
            res = self._exec(cmd)
            res = str(res).lower()
            if 'success' in res or 'complete' in res:
                logger.debug(f'app: {package_name}, uninstall ok')
            else:
                logger.debug(f'app: {package_name}, uninstall fail, error: {res}')

    def install(self, app_path: str, package_name: str, uninstall: bool = True,):
        if uninstall:
            self._uninstall(package_name)
        if self.plat == PLATFORM.AND:
            cmd = f'adb -s {self.did} install {app_path}'
        else:
            cmd = f'tidevice -u {self.did} install {app_path}'
        res = self._exec(cmd)
        res_str = str(res).lower()
        if 'success' in res_str or 'complete' in res_str:
            logger.info(f'app: {package_name}, install ok')
        else:
            logger.error(f'app: {package_name}, install fail, error: {res}')

    def app_version(self, package_name):
        assert self._is_install(package_name), f'need install app firstly !'
        if self.plat == PLATFORM.AND:
            cmd = f'adb -s {self.did} shell dumpsys package {package_name} | grep versionName'
            res = self._exec(cmd)
            return res[0].strip().split('=')[-1]
        else:
            cmd = f'tidevice -u {self.did} appinfo {package_name} ' \
                  f'| grep -E "CFBundleShortVersionString|CFBundleVersion"'
            res = self._exec(cmd)
            assert len(res) == 2
            part1, part2 = re.findall(r'\d+\.\d\.\d', res[0]), re.findall(r'\d+', res[1])
            return '.'.join(part1 + part2)


if __name__ == '__main__':
    # ins = Installer('ios', '00008020-001D1D900CB9002E')
    ins = Installer('android', 'TEV0217315000851')
    # ins._is_install('com.cctv.yangshipin.app.androidp')
    # ins.install('~/Downloads/YSP_v241.apk', 'com.cctv.yangshipin.app.androidp')
    # r = ins.app_version('com.cctv.yangshipin.app.iphone')
    r = ins.app_version('com.cctv.yangshipin.app.androidp')
    print(r)
    # import re
    # r = re.search(r'\d+\.\d\.\d', " 'CFBundleShortVersionString': '2.4.2',\n")
    # print(r.group())
