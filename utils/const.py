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
        'TEV0217315000851': '55954f5f7306287a',  # mate9pro
        'UMX0220C23004116': '6a646c25d5b51854',  # nova 7
        'XPL0219C18016526': '',  # mate 30
        'TTNGK21603000006': '',  # honor 30 pro+
        '5EF0217B22004759': '862005033754918',  # mate 9
        '9cc46ae4': '4781d134675f6f6d',  # OPPO k9
    }

    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4f6d76a7-d711-4576-868c-22eec500281f'
    chat_id = {
        # 'perf_test_group_chat': 'wrkSFfCgAASzYjXnG09u98JKCkT8xZQw',  # 专项测试群
        # 'ysp_qa_group_chat': 'wrkSFfCgAAU8wcbOJGm9OjPdiL7cs3iQ',  # 客户端质量保障群
        'debug_group_chat': 'wrkSFfCgAAg2dp_fLcZW7ct9idQKSmEQ'  # tapd机器人调试群
    }

    result_url = 'http://devops.oa.com/console/pipeline/{project_name}/{pipeline_id}/' \
                 'detail/{build_id}/output'

    content_tmpl = '## 启动耗时测试结果[[详情]({report_url})]\n' \
                   '\n' \
                   '> 平台: {platform}\n' \
                   '> 设备: {model}\n' \
                   '> 系统: {os_version}\n' \
                   '> 商店包版本: {store_app_ver}\n' \
                   '> 测试包版本: {test_app_ver}\n' \
                   '\n## 启动数据详情(ms)\n' \
                   '> **启动阶段 | 商店包 | 测试包 | 对比 **\n' \
                   '> {each_stage_detail_str}'
    each_stage_tmpl = '{stage} | {store_app_time} | {test_app_time} | {compare_result}'

    tmp_store_app_path = {
        PLATFORM.AND: '/Users/ssfanli/Desktop/store_app/ysp241.apk',
        PLATFORM.IOS: '/Users/ssfanli/Desktop/store_app/ysp241.ipa'
    }


if __name__ == '__main__':
    import pprint
    # pprint.pprint(COMMON.content_tmpl)
    print(COMMON.content_tmpl)
    tmp = {'platform': 'android', 'model': 'HOM-A100', 'os_version': '9.0',
           'store_app_ver': '2.4.1.12345', 'test_app_ver': '2.4.2.12345',
           'each_stage_detail': [
               {'stage': '程序启动', 'store_app_time': '120.0', 'test_app_time': '130.0', 'compare_result': '+10'},
               {'stage': '广告加载', 'store_app_time': '600.0', 'test_app_time': '500.0', 'compare_result': '-100'},
               {'stage': '真实启动', 'store_app_time': '720.0', 'test_app_time': '820.0', 'compare_result': '+100'}
           ]
           }