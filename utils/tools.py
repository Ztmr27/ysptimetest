#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: Ssfanli
@Time  : 2020/07/09 13:59
@Desc  : video cut
"""
import functools
import json
import os
import typing
from loguru import logger
from pathlib import Path
import requests as req

from utils.const import COMMON


def cut(original_video: typing.Union[str, os.PathLike],
        new_video: typing.Union[str, os.PathLike],
        start: str = '00:00:01',
        delete: bool = True):
    """video cut wrapper

    solve the blue screen at the beginning of ios video
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            cmd = f'ffmpeg -y -ss {start} -i {original_video} -c copy {new_video}'
            del_cmd = f'echo "delete original video ..." ; rm -rf {original_video}'
            if delete:
                cmd = cmd + ' && ' + del_cmd
            logger.debug(f"cut_cmd: {cmd}")
            os.system(cmd)
        return wrapper
    return decorator


def splice(*x):
    return os.path.join(*x)


def path_obj(p):
    return Path(p)


def abspath(p):
    return path_obj(splice(os.path.dirname(__file__), p)).resolve()


def file_exist(_fp, raise_error=True):
    """
    check the _fp exists
    :param _fp: file path
    :param raise_error: whether raise error
    :return:
    """
    if raise_error:
        if not os.path.exists(_fp):
            raise FileExistsError('file: %s dose not exists !' % _fp)
    else:
        return os.path.exists(_fp)


def md(_dir):
    if not file_exist(_dir, raise_error=False):
        os.makedirs(_dir)
    return _dir


def json_read(fp: str):
    with open(fp, 'r') as rf:
        return json.load(rf)


def json_write(fp: str, content, indent=2):
    with open(fp, 'w') as wf:
        json.dump(content, wf, indent=indent)


def avg(nums: list, decimal: int = 2) -> float:
    """calc nums average"""
    assert nums
    assert decimal >= 0
    cnt = 0
    lth = len(nums)
    for n in nums:
        cnt += n
    return round(cnt / lth, decimal)


def sender(content: str, to: str = 'debug_group_chat'):
    chat_ids = COMMON.chat_id
    assert to in chat_ids.keys()
    _data = {
        "msgtype": "markdown",
        "chatid": chat_ids[to],
        "markdown": {
            "content": content
        }
    }
    res = req.post(COMMON.send_url, json.dumps(_data))
    assert res.status_code == 200
    print(f'send success\n'
          f'content: \n{content}')


if __name__ == '__main__':
    # print(splice('../output', 'ysp'))
    # l = [{'time': '2022-03-03 19:37:51', 'data': {'et': 1000, 'tsm': 1646307471069, 'idx': 56, 'av': '2.4.2.66007', 'cui': '4dbf616d3bab11eca4646c92bf645f76', 'mid': 'none', 'mc': '02:00:00:00:00:00', 'ky': '867DD3AC8BF0', 'ifv': 'E4BB846D-39B8-4044-AF9E-DDD6A406E3E6', 'ui': 'a86169b44534309e6cf480229d40f3f1a42a5e9e', 'sv': '0.5.5.011', 'ch': 'appstore', 'ei': 'imp', 'kv': {'mac': '', 'sina_openid': '', 'call_from': '', 'is_vip': '0', 'location': '2', 'usid': '27840653-59D3-4552-B8E4-5817E8DF9805', 'network_type': '1', 'wx_openid': '', 'apple_userid': '', 'ref_page_id': '', 'jlbrk': '2', 'is_goto_online': '1', 'yangbizid': 'f0a91b8f698fa74fc9cbaae3cd8cbe6862db2bb0117203', 'main_login': '0', 'dev_model': 'iPhone 13 pro', 'udf_kv': {'ad_sdk': 20211008001, 'key_stage': {'launch_end_time': 1646307463.932846, 'progress_create_time': 1646307463.761021, 'finish_launch_end_time': 1646307463.9257112, 'total_launch_duration': 197.59297370910645, 'finish_launch_start_time': 1646307463.859478, 'main_method_start_time': 1646307463.8397331, 'finish_launch_total_duration': 66.23315811157227}, 'ad_type': 2, 'eid': 'app_launch_time', 'app_type': 1, 'material_type': 0, 'ad_load_time': 341.60780906677246, 'launch_time': 66.23315811157227, 'ad_load_timeout': False, 'request_adid_time': 0.11929082870483398, 'is_reinstall': False}, 'app_vr': '2.4.2.66007', 'channel_id': '50003', 'mf': 'apple', 'bucket_id': 'video_tab_mix_rec:video_tab_old_cms|variety_show_tab_mix_rec:variety_show_tab_old_cms|screen_player_test:blank|vertical_rec_test:blank|music_tab_mix_rec:music_tab_old_cms|kid_tab_mix_rec:kid_tab_old_cms|animation_tab_mix_rec:animation_tab_old_cms|car_tab_mix_rec:car_tab_old_cms|food_tab_mix_rec:food_tab_old_cms|record_tab_mix_rec:record_tab_old_cms|law_tab_mix_rec:law_tab_old_cms|culture_history_tab_mix_rec:culture_history_tab_old_cms', 'vuserid': '', 'idfv': 'E4BB846D-39B8-4044-AF9E-DDD6A406E3E6', 'idfa': '41323116-AA35-4F57-A438-8D8751CB901E', 'yangid': '3e10af6390bc9544872bd3511936c07d97230010117203', 'wx_commid': '', 'call_type': 1, 'os': '2', 'qq_openid': '', 'us_stmp': 1646307464094, 'user_strategy_id': '0ee907eb561954cfa664a811000011d15b02', 'os_vrsn': '15.0.2', 'qq': '', 'app_bld': '', 'pt': '7', 'page_id': '', 'guid': '4dbf616d3bab11eca4646c92bf645f76', 'page_step': '0'}, 'si': 969422650, 'ts': 1646307471, 'dts': 0, 'cav': '2.4.2.66007', 'rst': 0, 'id': 1203446657, 'ip': '111.206.145.22', 'sts': 1646307471}}, {'time': '2022-03-03 19:37:34', 'data': {'et': 1000, 'tsm': 1646307454021, 'idx': 55, 'av': '2.4.2.66007', 'cui': '4dbf616d3bab11eca4646c92bf645f76', 'mid': 'none', 'mc': '02:00:00:00:00:00', 'ky': '867DD3AC8BF0', 'ifv': 'E4BB846D-39B8-4044-AF9E-DDD6A406E3E6', 'ui': 'a86169b44534309e6cf480229d40f3f1a42a5e9e', 'sv': '0.5.5.011', 'ch': 'appstore', 'ei': 'imp', 'kv': {'mac': '', 'sina_openid': '', 'call_from': '', 'is_vip': '0', 'location': '2', 'usid': 'F648B30B-20F7-46D3-82E7-0BA560D88C01', 'network_type': '1', 'wx_openid': '', 'apple_userid': '', 'ref_page_id': '', 'jlbrk': '2', 'is_goto_online': '1', 'yangbizid': 'f0a91b8f698fa74fc9cbaae3cd8cbe6862db2bb0117203', 'main_login': '0', 'dev_model': 'iPhone 13 pro', 'udf_kv': {'ad_sdk': 20211008001, 'key_stage': {'launch_end_time': 1646307446.7663841, 'progress_create_time': 1646307446.599705, 'finish_launch_end_time': 1646307446.759653, 'total_launch_duration': 195.40977478027344, 'finish_launch_start_time': 1646307446.693397, 'main_method_start_time': 1646307446.676063, 'finish_launch_total_duration': 66.25604629516602}, 'ad_type': 2, 'eid': 'app_launch_time', 'app_type': 1, 'material_type': 0, 'ad_load_time': 83.52303504943848, 'launch_time': 66.25604629516602, 'ad_load_timeout': False, 'request_adid_time': 0.12487506866455078, 'is_reinstall': False}, 'app_vr': '2.4.2.66007', 'channel_id': '50003', 'mf': 'apple', 'bucket_id': 'video_tab_mix_rec:video_tab_old_cms|variety_show_tab_mix_rec:variety_show_tab_old_cms|screen_player_test:blank|vertical_rec_test:blank|music_tab_mix_rec:music_tab_old_cms|kid_tab_mix_rec:kid_tab_old_cms|animation_tab_mix_rec:animation_tab_old_cms|car_tab_mix_rec:car_tab_old_cms|food_tab_mix_rec:food_tab_old_cms|record_tab_mix_rec:record_tab_old_cms|law_tab_mix_rec:law_tab_old_cms|culture_history_tab_mix_rec:culture_history_tab_old_cms', 'vuserid': '', 'idfv': 'E4BB846D-39B8-4044-AF9E-DDD6A406E3E6', 'idfa': '41323116-AA35-4F57-A438-8D8751CB901E', 'yangid': '3e10af6390bc9544872bd3511936c07d97230010117203', 'wx_commid': '', 'call_type': 1, 'os': '2', 'qq_openid': '', 'us_stmp': 1646307446934, 'user_strategy_id': '0ee907eb561954cfa664a811000011d15b02', 'os_vrsn': '15.0.2', 'qq': '', 'app_bld': '', 'pt': '7', 'page_id': '', 'guid': '4dbf616d3bab11eca4646c92bf645f76', 'page_step': '0'}, 'si': 3116254282, 'ts': 1646307454, 'dts': 1, 'cav': '2.4.2.66007', 'rst': 0, 'id': 1203446657, 'ip': '111.206.145.22', 'sts': 1646307454}}]
    # l2 = [{'time': '2022-03-03 17:53:34', 'data': {'ei': 'imp', 'du': 1, 'kv': {'os_vrsn': 28, 'network_type': 1, 'qq': '', 'bucket_id': 'video_tab_mix_rec:video_tab_new_rec:blacklist|variety_show_tab_mix_rec:variety_show_tab_new_rec:blacklist|record_tab_mix_rec:record_tab_new_rec:blacklist|law_tab_mix_rec:law_tab_new_rec:blacklist|culture_history_tab_mix_rec:culture_history_tab_new_rec:blacklist', 'imei': '', 'android_id': '55954f5f7306287a', 'call_type': 1, 'user_strategy_id': '0c08f44956342e38afeb6cd3100018414a10', 'dev_model': 'LON-AL00', 'mac': '', 'main_login': 2, 'wx_openid': '', 'wx_commid': '', 'os': 1, 'yangbizid': '0a6b25381127024e9e996c090c40dd9367502bc0214716', 'channel_id': 51, 'sina_openid': '', 'dev_brand': 'HUAWEI', 'is_vip': '1', 'guid': '6d1fc2449a6411ec90a46c92bfd79530', 'yangid': '170ec2ffbd849f4fcf4ba463a473a9033a13001021330c', 'udf_kv': {'launch_time': 173, 'eid': 'app_launch_time', 'ad_load_time': 674, 'app_type': 1, 'ad_type': 2, 'key_stage': {'app_oncreate': 49, 'app_attach': 35, 'home_oncreate': 89}, 'ad_sdk': '', 'is_reinstall': False, 'in_splash_overtime': '0', 'vuid': '142240477'}, 'is_goto_online': '0', 'imsi': '', 'qq_openid': 'FE0CB1895AF550737A49D8E4E2D0912E', 'app_vr': '2.4.2.66009', 'vuserid': '142240477', 'screen_res': '1080*1920'}, 'os': 1, 'ov': '28', 'md': 'LON-AL00', 'jb': 0, 'mf': 'HUAWEI', 'tsm': 1646301219432, 'ky': 'B4F56A5103F9', 'ui': '55954f5f7306287a', 'mc': '30:74:96:27:3B:E5', 'si': 1300225217, 'et': 1000, 'ts': 1646301219, 'idx': 32062, 'cui': '55954f5f7306287a', 'ut': 0, 'av': '2.4.2.66009', 'ch': '51', 'dts': 0, 'mid': '', 'sv': '5.1.9.012', 'rst': 0, 'id': 1134692339, 'ip': '111.206.145.111', 'sts': 1646301214}}, {'time': '2022-03-03 17:56:03', 'data': {'ei': 'imp', 'du': 1, 'kv': {'os_vrsn': 28, 'network_type': 1, 'qq': '', 'imei': '', 'android_id': '55954f5f7306287a', 'call_type': 1, 'user_strategy_id': '0c08f44956342e38afeb6cd3100018414a10', 'dev_model': 'LON-AL00', 'mac': '', 'main_login': 0, 'wx_openid': '', 'wx_commid': '', 'os': 1, 'yangbizid': '0a6b25381127024e9e996c090c40dd9367502bc0214716', 'channel_id': 10001, 'sina_openid': '', 'dev_brand': 'HUAWEI', 'is_vip': '0', 'call_from': '', 'guid': '189749209ad811ec93b96c92bf645f76', 'yangid': '170ec2ffbd849f4fcf4ba463a473a9033a13001021330c', 'udf_kv': {'launch_time': 353, 'eid': 'app_launch_time', 'app_type': 1, 'key_stage': {'app_oncreate': 227, 'app_attach': 55, 'home_oncreate': 71}, 'ad_sdk': '', 'is_reinstall': True, 'in_splash_overtime': '0', 'vuid': ''}, 'is_goto_online': '1', 'imsi': '', 'qq_openid': '', 'app_vr': '2.4.1.51345', 'vuserid': '', 'screen_res': '1080*1920'}, 'os': 1, 'ov': '28', 'md': 'LON-AL00', 'jb': 0, 'mf': 'HUAWEI', 'tsm': 1646301368065, 'ky': 'B4F56A5103F9', 'ui': '55954f5f7306287a', 'mc': '30:74:96:27:3B:E5', 'si': 451521126, 'et': 1000, 'ts': 1646301368, 'idx': 60, 'cui': '55954f5f7306287a', 'ut': 0, 'av': '2.4.1.51345', 'ch': '10001', 'dts': 0, 'mid': '', 'sv': '5.1.9.012', 'rst': 0, 'id': 1134692339, 'ip': '111.206.145.111', 'sts': 1646301363}}, {'time': '2022-03-03 17:59:45', 'data': {'ei': 'imp', 'du': 1, 'kv': {'os_vrsn': 28, 'network_type': 1, 'qq': '', 'imei': '', 'android_id': '55954f5f7306287a', 'call_type': 1, 'user_strategy_id': '0c08f44956342e38afeb6cd3100018414a10', 'dev_model': 'LON-AL00', 'mac': '', 'main_login': 0, 'wx_openid': '', 'wx_commid': '', 'os': 1, 'yangbizid': '0a6b25381127024e9e996c090c40dd9367502bc0214716', 'channel_id': 10001, 'sina_openid': '', 'dev_brand': 'HUAWEI', 'is_vip': '0', 'call_from': '', 'guid': '9d9347fb9ad811ec93b96c92bf645f76', 'yangid': '170ec2ffbd849f4fcf4ba463a473a9033a13001021330c', 'udf_kv': {'launch_time': 279, 'eid': 'app_launch_time', 'app_type': 1, 'key_stage': {'app_oncreate': 180, 'app_attach': 33, 'home_oncreate': 66}, 'ad_sdk': '', 'is_reinstall': True, 'in_splash_overtime': '0', 'vuid': ''}, 'is_goto_online': '1', 'imsi': '', 'qq_openid': '', 'app_vr': '2.4.1.51345', 'vuserid': '', 'screen_res': '1080*1920'}, 'os': 1, 'ov': '28', 'md': 'LON-AL00', 'jb': 0, 'mf': 'HUAWEI', 'tsm': 1646301590555, 'ky': 'B4F56A5103F9', 'ui': '55954f5f7306287a', 'mc': '30:74:96:27:3B:E5', 'si': 421938985, 'et': 1000, 'ts': 1646301590, 'idx': 47, 'cui': '55954f5f7306287a', 'ut': 0, 'av': '2.4.1.51345', 'ch': '10001', 'dts': 0, 'mid': '', 'sv': '5.1.9.012', 'rst': 0, 'id': 1134692339, 'ip': '111.206.145.111', 'sts': 1646301585}}]
    # # json_write('../output/tmp.json', l)
    # json_write('../output/tmp2.json', l2)
    sender('test')