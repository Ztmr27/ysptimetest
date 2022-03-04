#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Ssfanli
@Time  : 2019/10/22 18:55
@Desc  : Json常用操作封装
"""

import os
import json
from public.base_device import AndroidDevice, IOSDevice
from public.base_path import P
from public.base_config_parser import cfg


class DeviceInfo(object):
    """"""
    def __init__(self, platform: str):
        self.pfm = platform.lower()
        assert self.pfm in ('a', 'android', 'i', 'ios'), f"platform should in ('a', 'android', 'i', 'ios')"
        if self.pfm in ('a', 'android'):
            self.device = AndroidDevice()
            self.path = P(cfg().get('Path', 'aphone'))
        else:
            self.device = IOSDevice()
            self.path = P(cfg().get('Path', 'iphone'))

    def write_device_info_to_json(self, _device_id):
        """
        写device_info
        :return:
        """
        with open(self.path, 'w') as wf:
            json.dump(self.device.device_info(_device_id), wf)

    def update_device_info(self):
        """
        1. 更新device_info到json文件
        2. 只从连接的设备列表中取第一个device_id，
        3. TODO: 后续完善多设备连接情况的选择逻辑
        :return:
        """
        cur_device_id = self.device.get_device_id()[0]
        if not os.path.exists(self.path) or cur_device_id != self.info['id']:
            self.write_device_info_to_json(cur_device_id)

    @property
    def info(self):
        """
        获取device_info json
        :return:
        """
        with open(self.path, 'r') as rf:
            return json.load(rf)

    def __call__(self):
        return self.info


if __name__ == '__main__':
    d = DeviceInfo('i')
    d.update_device_info()

