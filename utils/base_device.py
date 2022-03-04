#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Lidi
@Time  : 2019/5/19 22:02
@Desc  : Encapsulation of base adb command
"""

import os
from loguru import logger
from public.base_path import P


class AndroidDevice(object):

    """The class is aimed at encapsulating base adb command """

    @staticmethod
    def adb(cmd):
        """
        return the result of executing command
        :param cmd:
        :return:
        """
        return os.popen('adb %s' % cmd, 'r')

    def get_device_id(self):
        """
        get device ID
        :return:
        """
        cmd = 'devices'
        device_id = []
        res = self.adb(cmd).readlines()
        for i in res:
            devices = i.split('\tdevice')
            if len(devices) >= 2:
                device_id.append(devices[0])
        logger.info('device_id list is: %s' % device_id)
        return device_id

    def get_android_ver(self, device_id):
        """
        get the device's android version
        :param device_id:
        :return:
        """
        cmd = '-s %s shell getprop ro.build.version.release' % device_id
        res = self.adb(cmd).read()
        android_ver = res.split('\n')[0]
        logger.info('android version is: %s' % android_ver)
        return android_ver

    def get_sdk_ver(self, device_id):
        """
        get the device's android  SDK version
        :param device_id:
        :return:
        """
        cmd = '-s %s shell getprop ro.build.version.sdk' % device_id
        res = self.adb(cmd).read()
        android_ver = res.split('\n')[0]
        logger.info('android sdk version is: %s' % android_ver)
        return android_ver

    def get_device_model(self, device_id):
        """
        获取设备型号
        :param device_id:
        :return:
        """
        cmd = '-s %s shell getprop ro.product.model' % device_id
        res = self.adb(cmd).read()
        model = res.split('\n')[0]
        logger.info('current device model is: %s' % model)
        return model

    def get_device_brand(self, device_id):
        """
        获取设备品牌
        :param device_id:
        :return:
        """
        cmd = '-s %s shell getprop ro.product.brand' % device_id
        res = self.adb(cmd).read()
        model = res.split('\n')[0]
        logger.info('current device brand is: %s' % model)
        return model

    def get_device_rom(self, device_id):
        """
        获取设备ROM名，如：MHA-AL00C00B213
        :param device_id:
        :return:
        """
        cmd = '-s %s shell getprop ro.build.display.id' % device_id
        res = self.adb(cmd).read()
        model = res.split('\n')[0]
        logger.info('current device rom is: %s' % model)
        return model

    def device_info(self, device_id):
        """
        获取当前设备全部信息，返回字典型
        :param device_id:
        :return:
        """
        info = {}
        info['id'] = device_id
        info['brand'] = self.get_device_brand(device_id)
        info['model'] = self.get_device_model(device_id)
        info['os_version'] = self.get_android_ver(device_id)
        info['sdk_version'] = self.get_sdk_ver(device_id)
        info['rom_version'] = self.get_device_rom(device_id)
        logger.info('device_info is: %s' % info)
        return info


class IOSDevice(object):

    """The class is aimed at encapsulating base adb command """

    # update here dict when a new iphone release
    iOSDeviceMap = {
        'iPhone3,1': 'iPhone 4',
        'iPhone3,2': 'iPhone 4',
        'iPhone3,3': 'iPhone 4',
        'iPhone4,1': 'iPhone 4S',
        'iPhone5,1': 'iPhone 5',
        'iPhone5,2': 'iPhone 5',
        'iPhone5,3': 'iPhone 5c',
        'iPhone5,4': 'iPhone 5c',
        'iPhone6,1': 'iPhone 5s',
        'iPhone6,2': 'iPhone 5s',
        'iPhone7,1': 'iPhone 6 Plus',
        'iPhone7,2': 'iPhone 6',
        'iPhone8,1': 'iPhone 6s',
        'iPhone8,2': 'iPhone 6s Plus',
        'iPhone8,4': 'iPhone SE',
        'iPhone9,1': 'iPhone 7',
        'iPhone9,2': 'iPhone 7 Plus',
        'iPhone9,3': 'iPhone 7',
        'iPhone9,4': 'iPhone 7 Plus',
        'iPhone10,1': 'iPhone 8',
        'iPhone10,2': 'iPhone 8 Plus',
        'iPhone10,4': 'iPhone 8',
        'iPhone10,5': 'iPhone 8 Plus',
        'iPhone10,3': 'iPhone X',
        'iPhone10,6': 'iPhone X',
        'iPhone11,2': 'iPhone XS',
        'iPhone11,4': 'iPhone XS Max',
        'iPhone11,6': 'iPhone XS Max',
        'iPhone11,8': 'iPhone XR',
        'iPhone12,1': 'iPhone 11',
        'iPhone12,3': 'iPhone 11 Pro',
        'iPhone12,5': 'iPhone 11 Pro Max',
    }

    @staticmethod
    def exec(cmd):
        """
        return the result of executing command
        :param cmd:
        :return:
        """
        return os.popen('%s' % cmd, 'r')

    def get_device_id(self):
        """get device ID

        idevice_id -l 当设备和电脑在一个局域网下，会获取USB和WiFi两个udid
        存在当设备已经断开连接但依然还可以获取udid的问题
        """
        cmd = P('../shell/udid.sh')
        device_id = []
        res = self.exec(cmd).readlines()
        for i in res:
            device_id.append(i.strip())
        assert device_id, f'No device found !'
        logger.info('device_id is: %s' % device_id)
        return device_id

    def get_device_model(self, device_id):
        """
        get the device's type
        :param device_id:
        :return:
        """
        cmd = 'ideviceinfo -u %s -k ProductType' % device_id
        res = self.exec(cmd).read()
        _type = res.strip('\n')
        device_type = self.iOSDeviceMap.get(_type)
        logger.info('device_type is: %s' % device_type)
        return device_type

    def get_device_ver(self, device_id):
        """
        get the device's version
        :param device_id:
        :return:
        """
        cmd = 'ideviceinfo -u %s -k ProductVersion' % device_id
        res = self.exec(cmd).read()
        device_ver = res.strip('\n')
        logger.info('device_ver is: %s' % device_ver)
        return device_ver

    def get_device_name(self, device_id):
        """
        get device name
        :param device_id:
        :return:
        """
        cmd = 'idevicename -u %s' % device_id
        res = self.exec(cmd).read()
        device_name = res.strip('\n')
        logger.info('device_ver is: %s' % device_name)
        return device_name

    def device_info(self, device_id):
        """"""
        info = {}
        info['id'] = device_id
        info['version'] = self.get_device_ver(device_id)
        info['device_name'] = self.get_device_name(device_id)
        info['model'] = self.get_device_model(device_id)
        logger.info('device_info is: %s' % info)
        return info


if __name__ == '__main__':
    i = IOSDevice()
    i.get_device_id()
    # i = AndroidDevice()
    # uid = i.get_device_id()[0]
    # i.device_info(uid)
