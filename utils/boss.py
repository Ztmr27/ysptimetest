# -*- coding: utf-8 -*- 
"""Created by ssfanli on 2021/12/19 
"""
import json
import re
import time
import typing
import sys

import requests as req
from loguru import logger
from bs4 import BeautifulSoup

logger.add('../output/app_launch_time.log', format="{message}", filter="", level="INFO")

BOSS_MAPPING = {'android': {'ftype': 'ui', 'appid': '1134692339'},
                'ios': {'ftype': 'ifv', 'appid': '1203446657'}}


def avg(nums: list, decimal: int = 2) -> float:
    """calc nums average"""
    assert nums
    assert decimal >= 0
    cnt = 0
    lth = len(nums)
    for n in nums:
        cnt += n
    return round(cnt / lth, decimal)


def _now(fmt: str = 'YmdHMS'):
    """return now

    `YmdHMS`
    """
    _fmt = ''
    for s in list(fmt):
        if s.isalpha():
            _fmt += '%' + s
        else:
            _fmt += s
    return time.strftime(_fmt or fmt)


class BossHelper(object):
    """BossHelper

    get report data from boss

    attention: network must in Tencent-WiFi and add such content in /etc/hosts
    ```sh
    140.143.213.139 beehive.boss.video.cloud.cctv.com
    140.143.213.139 auth.video.cloud.cctv.com
    ```
    """

    def __init__(self, platform, div_id):
        """
        platform: android, ios
        div_id: imei or androidid if os is android else idfv
        """
        assert platform in BOSS_MAPPING
        self.div_id = div_id
        self.plat = platform
        self.ftype = BOSS_MAPPING[self.plat]['ftype']
        self.appid = BOSS_MAPPING[self.plat]['appid']
        self.date = _now('Y-m-d')
        self._init_device()

    # TODO: no used
    def get_con(self):
        url = 'http://beehive.boss.video.cloud.cctv.com/mobile/real/getCon'
        ts = int(time.time() * 1000)
        params = {'ftype': self.ftype, 'keyword': self.div_id, 'pageSize': 10, 'pageNo': 1,
                  'extra': '', '_': ts}
        rsp = req.get(url, params=params)
        res = rsp.text
        logger.debug(f'device_register response: {res}')
        return self.div_id in res

    def _init_device(self):
        url = 'http://beehive.boss.video.cloud.cctv.com/mobile/real/listConDataCount'
        params = {'_dc': '', 'sortField': 'ftime', 'sortType': 'desc', 'pageNo': 1, 'pageSize': 15,
                  'appid': self.appid, 'qtype': 'app', 'plat': self.plat, 'odktag': 1, 'ftype': self.ftype,
                  'filterKeyword': '', 'eventid': '', 'diviseid': self.div_id, 'filterdate': self.date
                  }
        rsp = req.get(url, params=params)
        error_code, rsp_info = rsp.status_code, rsp.text
        assert error_code == 200, 'init device failed:' \
                                  '\n1. status_code: {}' \
                                  '\n2. error_info: \n{}'.format(error_code, rsp_info)
        logger.debug('device: {}, init ok: {}'.format(self.div_id, rsp_info))

    def get_data(self,
                 eid: str = '',
                 keyword: str = '',
                 page_size: int = 10,
                 conversion: bool = False):
        """get data from boss

        eid: event_id, such as: imp, clck
        keyword: such as: app_launch_time
        page_size: control get N pieces of data

        :return: list[dict[str: str]]
            [{'time': '2021-12-20 07:56:00', 'data': '{"et":1000, ...}'}, ...]
        """
        url = 'http://beehive.boss.video.cloud.cctv.com/mobile/real/listConData'
        params = {'_dc': '', 'sortField': 'ftime', 'sortType': 'desc', 'pageNo': 1, 'pageSize': page_size,
                  'appid': self.appid, 'qtype': 'app', 'plat': self.plat, 'odktag': 1, 'ftype': self.ftype,
                  'filterKeyword': keyword, 'eventid': eid, 'diviseid': self.div_id, 'filterdate': self.date
                  }
        rsp = req.get(url, params=params)
        error_code, rsp_info = rsp.status_code, rsp.text
        assert error_code == 200, 'get_data failed:' \
                                  '\n1. status_code: {}' \
                                  '\n2. error_info: \n{}'.format(error_code, rsp_info)

        bfs = BeautifulSoup(rsp.text, 'lxml')
        time_cmp = re.compile(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}')
        ret = []
        for td_time, td_data in zip(bfs.find_all('td', title=time_cmp), bfs.find_all('td', class_='myjson')):
            tmp = {'time': td_time.text,
                   'data': json.loads(td_data.text) if conversion else td_data.text}
            ret.append(tmp)
        return ret

    @staticmethod
    def data_analysis(data_list: typing.List[dict]):
        data_list_asc = sorted(data_list, key=lambda x: x['time'])
        logger.debug(f'\ndata_list: {data_list}'
                     f'\ndata_list_asc: {data_list_asc}')

        start_idx, end_idx = 0, len(data_list)

        new_data_list = data_list_asc[start_idx: end_idx]
        launch_time_data_list_zd_ad = []
        launch_time_data_list_cms_ad = []
        launch_time_data_list_no_ad = []
        for data in new_data_list:
            report_data = data.get('data')
            report_time = data.get('time')

            if not report_data or not report_time:
                continue
            tmp = {'report_time': report_time}
            os = report_data.get('kv').get('os')
            udf_kv = report_data.get('kv').get('udf_kv')
            if udf_kv:
                if os and str(os) == '1':
                    ad_type = udf_kv.get('ad_type')
                    in_splash_overtime = udf_kv.get('in_splash_overtime')
                    launch_time = udf_kv.get('launch_time', 0)
                    request_adid_time = udf_kv.get('request_adid_time', 0)
                    ad_load_time = udf_kv.get('ad_load_time', 0)
                    if isinstance(ad_load_time, str):
                        ad_load_time = int(ad_load_time.replace('ms', ''))
                    request_adid_timeout = udf_kv.get('request_adid_timeout', False)
                    ad_load_timeout = udf_kv.get('ad_load_timeout', False)
                    if in_splash_overtime == '1':
                        real_launch_time = launch_time
                    else:
                        if ad_type == 1:
                            real_launch_time = launch_time + request_adid_time + ad_load_time
                        elif ad_type == 2:
                            real_launch_time = launch_time + ad_load_time
                        else:
                            real_launch_time = -1
                    tmp.update(ad_type=ad_type,
                               launch_time=launch_time,
                               request_adid_time=request_adid_time,
                               ad_load_time=ad_load_time,
                               request_adid_timeout=request_adid_timeout,
                               ad_load_timeout=ad_load_timeout,
                               real_launch_time=real_launch_time)
                    if in_splash_overtime == '1':
                        launch_time_data_list_no_ad.append(tmp)
                    else:
                        if ad_type == 1:
                            launch_time_data_list_cms_ad.append(tmp)
                        elif ad_type == 2:
                            launch_time_data_list_zd_ad.append(tmp)
                        else:
                            raise
                elif os and str(os) == '2':
                    ad_type = udf_kv.get('ad_type')
                    launch_time = udf_kv.get('launch_time', 0)
                    ad_load_time = udf_kv.get('ad_load_time', 0)
                    if isinstance(ad_load_time, str):
                        ad_load_time = int(ad_load_time.replace('ms', ''))
                    ad_load_timeout = udf_kv.get('ad_load_timeout')
                    if not ad_type or ad_type == 0:
                        real_launch_time = launch_time
                    else:
                        real_launch_time = launch_time + ad_load_time
                    tmp.update(ad_type=ad_type,
                               launch_time=launch_time,
                               ad_load_time=ad_load_time,
                               ad_load_timeout=ad_load_timeout,
                               real_launch_time=real_launch_time)
                    if not ad_type or ad_type == 0:
                        launch_time_data_list_no_ad.append(tmp)
                    else:
                        if ad_type == 1:
                            launch_time_data_list_cms_ad.append(tmp)
                        elif ad_type == 2:
                            launch_time_data_list_zd_ad.append(tmp)
                        else:
                            raise

        if not launch_time_data_list_zd_ad and not launch_time_data_list_no_ad:
            raise

        def calc_print(dl):
            if not dl:
                return
            report_times = []
            launch_times = []
            real_launch_times = []
            request_adid_times = []
            ad_load_times = []
            for launch_time_data in dl:
                report_times.append(launch_time_data.get('report_time'))
                real_launch_times.append(launch_time_data.get('real_launch_time'))
                launch_times.append(launch_time_data.get('launch_time'))
                request_adid_times.append(launch_time_data.get('request_adid_time', 0))
                ad_load_times.append(launch_time_data.get('ad_load_time'))
            logger.info('%20s, %16s, %11s, %17s, %12s' %
                        ('report_time', 'real_launch_time', 'launch_time', 'request_adid_time', 'ad_load_time'))
            for report_time, real_launch_time, launch_time, request_adid_time, ad_load_time in zip(
                    report_times, real_launch_times, launch_times, request_adid_times, ad_load_times):
                logger.info('%20s, %16.2f, %11.2f, %17.2f, %12.2f' %
                            (report_time, real_launch_time, launch_time, request_adid_time, ad_load_time))
            logger.info('%20s, %16.2f, %11.2f, %17.2f, %12.2f' %
                        ('average', avg(real_launch_times), avg(launch_times),
                         avg(request_adid_times), avg(ad_load_times)))

        if launch_time_data_list_zd_ad:
            logger.info('中电广告耗时')
            calc_print(launch_time_data_list_zd_ad)
        if launch_time_data_list_cms_ad:
            logger.info('CMS广告耗时')
            calc_print(launch_time_data_list_cms_ad)
        if launch_time_data_list_no_ad:
            logger.info('无广告耗时')
            calc_print(launch_time_data_list_no_ad)


if __name__ == '__main__':
    # args = sys.argv
    # args = args[1:]
    # from pprint import pprint

    # 13pro: EA4B2FAA-C486-4716-8A99-1858F5FE1408
    # keke iphone12: C7DC6ACF-A6D0-404E-9E56-DDAA8521321D，FE7D77FC-2A91-4A88-AE4C-9A4B2D454C4D
    # oppo k9: android id: 4781d134675f6f6d
    # oppo find x2: android id: b0df9f2842fd2fee imei2: 868272048422972
    # my xr: 77B5E772-E16D-4A5C-B621-2163682AB60C
    # emma: d3035eeee2a1caa7
    # mate9: imei 862005033754918, android id: 0bc9cdaaf3b48252
    # mate9pro imei 864682039607148
    # nova7 6a646c25d5b51854
    bh = BossHelper('android', '6a646c25d5b51854')
    # bh = BossHelper('ios', 'FE7D77FC-2A91-4A88-AE4C-9A4B2D454C4D')
    r = bh.get_data(page_size=1, keyword='app_launch_time', conversion=True)
    bh.data_analysis(r)
