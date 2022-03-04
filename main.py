# -*- coding: utf-8 -*- 
"""Created by ssfanli on 2022/03/01 
"""
import sys

from loguru import logger

from case.ysp_start import YSPStart
from utils.boss import avg
from utils.tools import sender, json_read, splice
from utils.const import COMMON


def start_test(platform, device_id, test_app_path):
    ret = []
    for app_path in [COMMON.tmp_store_app_path[platform], test_app_path]:
        ysp = YSPStart(platform, device_id, app_path)
        app_ver, video_dir = ysp.cold_start(10)
        ret.append((app_ver, video_dir))
    return ret


def data_process(target_data_list, current_data_list):
    def calc(a, b):
        res = round(b - a, 1)
        if res >= 0:
            return f'+{res}'
        return str(res)

    def clean_data(app_ver, src_data):
        tmp = {'app_ver': app_ver}
        launch_time_list = []
        ad_load_time_list = []
        for data in src_data:
            kv = data['data']['kv']
            if app_ver != kv['app_vr']:
                continue
            if not tmp.get('model') and not tmp.get('os_version'):
                tmp['model'] = kv['dev_model']
                tmp['os_version'] = kv['os_vrsn']
            udf_kv = kv['udf_kv']
            launch_time = udf_kv.get('launch_time')
            ad_load_time = udf_kv.get('ad_load_time')
            if launch_time:
                launch_time_list.append(launch_time)
            if ad_load_time:
                ad_load_time_list.append(ad_load_time)
        tmp['launch_time_list'] = launch_time_list
        tmp['launch_time_avg'] = avg(launch_time_list, 1) if launch_time_list else 0.0
        tmp['ad_load_time_list'] = ad_load_time_list
        tmp['ad_load_time_avg'] = avg(ad_load_time_list, 1) if ad_load_time_list else 0.0
        tmp['real_launch_time'] = tmp['launch_time_avg'] + tmp['ad_load_time_avg']
        return tmp

    target_app_ver, target_app_path = target_data_list
    current_app_ver, current_app_path = current_data_list
    logger.info(f'\ntarget_data_list: {target_data_list}'
                f'\ncurrent_data_list: {current_data_list}')
    target_app_src_data = json_read(splice(target_app_path, 'report_data.json'))
    current_app_src_data = json_read(splice(current_app_path, 'report_data.json'))
    target_app_data = clean_data(target_app_ver, target_app_src_data)
    current_app_data = clean_data(current_app_ver, current_app_src_data)
    ret = {'store_app_ver': target_app_ver,
           'test_app_ver': current_app_ver,
           'model': target_app_data['model'],
           'os_version': target_app_data['os_version'],
           'each_stage_detail': [
               {'stage': '程序启动',
                'store_app_time': target_app_data['launch_time_avg'],
                'test_app_time': current_app_data['launch_time_avg'],
                'compare_result': calc(target_app_data['launch_time_avg'], current_app_data['launch_time_avg'])},
               {'stage': '广告加载',
                'store_app_time': target_app_data['ad_load_time_avg'],
                'test_app_time': current_app_data['ad_load_time_avg'],
                'compare_result': calc(target_app_data['ad_load_time_avg'], current_app_data['ad_load_time_avg'])},
               {'stage': '真实启动',
                'store_app_time': target_app_data['real_launch_time'],
                'test_app_time': current_app_data['real_launch_time'],
                'compare_result': calc(target_app_data['real_launch_time'], current_app_data['real_launch_time'])}
           ]
           }
    return ret


def generate_report(data):
    pass


def sent_result(data):
    content = COMMON.content_tmpl.format(
        report_url=COMMON.result_url,
        each_stage_detail_str='\n'.join(
            [COMMON.each_stage_tmpl.format(**d) for d in data['each_stage_detail']]),
        **data)
    sender(content)


if __name__ == '__main__':
    args = sys.argv
    args = args[1:]
    assert len(args) == 3, 'run such as: python3 main.py "platform" "device_id" "test_app_path"'
    logger.info(f'run args: {args}')
    target_test_res, current_test_res = start_test(args[0], args[1], args[2])
    test_data = data_process(target_test_res, current_test_res)
    test_data['platform'] = args[0]
    sent_result(test_data)

    # test_data = data_process(
    #     ('2.4.1.51345', '/Users/ssfanli/Myfolder/myproj/python/ysptimetest/output/ysp/and/2.4.1.51345'),
    #     ('2.4.2.66011', '/Users/ssfanli/Myfolder/myproj/python/ysptimetest/output/ysp/and/2.4.2.66011'))
    # test_data['platform'] = 'android'
    # import pprint
    # pprint.pprint(test_data)
    # sent_result(test_data)

    # , '/Users/ssfanli/Desktop/cctvvideo-ios_2.4.2.66007_enterprise_sign.ipa'
    # ysp = YSPStart('ios', '00008020-001D1D900CB9002E')
    # ysp.cold_start(3)
