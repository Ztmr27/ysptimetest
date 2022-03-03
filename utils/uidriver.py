# -*- coding: utf-8 -*- 
"""Created by ssfanli on 2022/03/01 
"""
import wda
import time
import uiautomator2 as u2
from loguru import logger

from utils.const import *

WHITELIST = {'跳过', '允许', '始终允许', '关闭', '同意', '以后', '再想想', '稍后', '稍后提醒我', '暂不升级', '取消', '好'}
BUTTON_CLASSNAME = {'className': 'XCUIElementTypeButton'}
STATIC_TEXT_CLASSNAME = {'className': 'XCUIElementTypeStaticText'}
TEXTFIELD_CLASSNAME = {'className': 'XCUIElementTypeTextField'}
ALERT_CLASSNAME = {'className': 'XCUIElementTypeAlert'}


# TODO:
#  1. init和BaseOperate拆开，init继承BaseOperate
#  2. 双端BaseOperate应该合并，参考loginhelper
#  3. 定位和代码分离，参考anduiauto
#  4. 初始化增加判断标志位？
class BaseOperateIOS(object):

    def __init__(self, udid: str, bundle_id: str = PACKAGE.YSP_IOS):
        # 因为不会有多设备运行，直接读取文件
        self.udid = udid
        self.bundle_id = bundle_id
        self.init_ok_flag_loc = {'label': '时事', **STATIC_TEXT_CLASSNAME, 'visible': True}
        self.client = wda.USBClient(self.udid, wda_bundle_id='.xctrunner')
        self.se = self.client.session(self.bundle_id)
        logger.debug(
            'Init WDA client session is success\nbundle_id: %s\nport: %s ' % (self.bundle_id, 8100))
        self.init_app()

    def start_ysp(self):
        self.client.app_start(self.bundle_id)
        self.init_app()
        return self

    def _close_notice_alert(self):
        notice_alert_loc = {'label': '“央视频”想给您发送通知', **ALERT_CLASSNAME}
        bn = ['不允许']
        if self.ele_exist(**notice_alert_loc):
            self._close_alert(bn)
            time.sleep(1)

    def _close_alert(self, black_name: list = None):
        if black_name is None:
            black_name = WHITELIST
        for name in black_name:
            if self.ele_exist(label=name, visible=True):
                self.to_click(label=name)

    def _ad_skip(self):
        skip_loc = {'labelContains': '跳过'}
        if self.ele_exist(**skip_loc):
            self.to_click(**skip_loc)

    def _process_guide(self, guide_flag: dict, repeat=10, wait: int = 1):
        count = 0
        if self.ele_exist(**self.init_ok_flag_loc):
            return
        while not self.ele_exist(**guide_flag) and count < repeat:
            logger.debug('swipe_left ...')
            self.se.swipe_left()
            time.sleep(wait)
            count += 1
        else:
            if count >= repeat:
                raise Exception('init_app error, exceeding limit!')
            else:
                self.to_click(**guide_flag)
                logger.debug('_process_guide success')
                time.sleep(2)

    def _process_privacy(self):
        privacy_loc = {'label': '用户协议及隐私政策概要', **STATIC_TEXT_CLASSNAME}
        bn = ['同意']
        if self.ele_exist(**privacy_loc):
            self._close_alert(bn)
            time.sleep(1)

    def _process_homepage_ad(self):
        home_flag_invisible_loc = {'label': '首页', **BUTTON_CLASSNAME}
        tmp = self.is_visible(timeout=0.5, **home_flag_invisible_loc)
        if tmp is not None and not tmp:
            self.to_click(**home_flag_invisible_loc)
            time.sleep(1)

    def init_app(self, flag: dict = None, guide_flag='newuser guide start', repeat=20, delay: int = 1):
        """处理弹窗回调"""
        guide_flag_loc = {'label': guide_flag, **BUTTON_CLASSNAME}
        count = 0
        self.timer(delay)
        self._ad_skip()
        while not self.ele_exist(**flag or self.init_ok_flag_loc) and count < repeat:
            logger.debug(f'try init {count + 1} ...')
            self._process_homepage_ad()
            self._close_notice_alert()
            self._close_alert()
            self._process_guide(guide_flag_loc)
            self._process_privacy()
            count += 1
        else:
            if count >= repeat:
                raise Exception('init_app error, exceeding limit!')
            else:
                logger.info('init app success')

    def to_click(self, elements: list = None, **loc):
        """to click pro wrapper

        elements, retry element list
        loc, location, kw
        """
        els = elements or WHITELIST

        def recovery():
            logger.warning(f'element: {loc} not found, try recovery ...')
            for ele in els:
                if self.ele_exist(label=ele):
                    self.se(label=ele).click()

        try:
            self.se(**loc).click(5)
            logger.debug(f'to_click_pro success, {loc}')
        except wda.WDAElementNotFoundError:
            recovery()
            self.se(**loc).click(1)

    def switch_to(self, tab):
        """switch to any tab when in any page
        """
        if self.auto_back:
            self.to_click(label=tab)
            time.sleep(1)
        else:
            raise Exception('auto_back error')

    @property
    def auto_back(self):
        """auto back from 2,3,4th page"""
        home_nav_loc = {'name': '首页'}
        back_btn = [
            '返回',
            'back',
            '取消',
            'close'
        ]

        if self.ele_exist(**home_nav_loc):
            return True
        else:
            for btn in back_btn:
                if self.ele_exist(labelContains=btn):
                    self.to_click(labelContains=btn)
                    time.sleep(.5)
                    return self.auto_back
            self.se.swipe_right()
            return self.auto_back

    def ele_exist(self, **loc):
        res = self.se(**loc).exists
        logger.debug(f'ele_exist: {loc}, {res}')
        return res

    def ele_text(self, **loc):
        ret = self.se(**loc).get(timeout=5)
        logger.debug(f'ele_text: {loc}, text: {ret.text}')
        return ret.text

    def is_visible(self, timeout: float = 1.0, **loc):
        ret = self.se(**loc).get(timeout=timeout, raise_error=False)
        if not ret:
            logger.debug(f'is_visible: {loc}, element not found')
            return ret
        if ret:
            res = ret.visible
            logger.debug(f'is_visible: {loc}, {res}')
            return res

    def send_keys(self, **kw):
        """
        输入内容
        :param kw: 定位坐标的key=value，以及输入的content=value
        :return:
        """
        if kw['content']:
            content = kw.pop('content')
            time.sleep(1)
            self.se(**kw).set_text(content)
            logger.debug('textfield input %s' % content)
            return True, content
        else:
            logger.debug('no content, please check!')
            return False, None

    def stop_apps(self, *bundle_id):
        for bid in bundle_id:
            self.se.app_stop(bid)
            time.sleep(1)

    def close_app(self):
        self.se.app_stop(self.bundle_id)
        logger.debug('close_app ...')

    @staticmethod
    def timer(t: int):
        for i in range(t):
            logger.debug('%ss ...' % (t - i))
            time.sleep(1)

    def get_idfv(self, close_app: bool = True):

        def _enter_about():
            self.switch_to('我的')
            time.sleep(1)
            for step in ['设置', '关于央视频']:
                if not self.ele_exist(label=step):
                    self.se.swipe_up()
                    time.sleep(.5)
                self.to_click(label=step)
                time.sleep(1)

        def _get_idfv():
            assert self.ele_exist(label='关于央视频')
            x, y, w, h = self.se(labelContains='版本').get(timeout=5).bounds
            count = 1
            while not self.ele_exist(label='上传日志') and count <= 20:
                self.se.click(x, y)
                count += 1
            else:
                if count > 20:
                    raise
            txt = self.ele_text(labelContains='IDFV')
            txt_list = txt.split()
            if txt and txt_list:
                return txt_list[txt_list.index('IDFV') + 1]
            raise KeyError(f'text or text_list is null !')

        _enter_about()
        idfv = _get_idfv()
        if close_app:
            self.close_app()
            time.sleep(1)
        return idfv

    def wait_for_appear(self, flag: str = '时事'):
        count = 1
        while not self.ele_exist(label=flag) and count <= 10:
            time.sleep(1)
            count += 1
        else:
            if count > 10:
                logger.warning(f'flag: {flag} not appear')
            else:
                logger.debug(f'flag: {flag} appear')


class BaseOperateAND(object):

    def __init__(self, device_id: str, package_name: str = PACKAGE.YSP_AND):
        """
        初始化
        :param package_name: 包名
        """
        self.pkg_name = package_name
        self.cur_device_id = device_id
        self.d = u2.connect_usb(self.cur_device_id)
        self.d.screen_on()
        self.init_app()

    @staticmethod
    def timer(t: int):
        for i in range(t):
            logger.debug('%ss ...' % (t - i))
            time.sleep(1)

    def _skip_ad(self):
        splash_container_loc = {'resourceId': 'com.cctv.yangshipin.app.androidp:id/splash_container'}
        if self.ele_exist(**splash_container_loc):
            self.d(textContains='跳过').click_exists(timeout=1)
            logger.debug('skip_ad ...')

    def _skip_homepage_ad(self):
        homepage_ad_close_loc = {'resourceId': 'com.cctv.yangshipin.app.androidp:id/ad_close'}
        if self.ele_exist(**homepage_ad_close_loc):
            self.d(**homepage_ad_close_loc).click_exists(timeout=1)
            logger.debug('skip_homepage_ad ...')

    def init_app(self, repeat: int = 20, delay: int = 3):
        app_current_page = ['com.tencent.videolite.android.ui.huawei.AgreementActivity',
                            'com.tencent.videolite.android.ui.SplashActivity',
                            'com.tencent.videolite.android.ui.GuidePageActivity',
                            'com.android.packageinstaller.permission.ui.GrantPermissionsActivity']
        init_list = [{'text': '同意', 'wait': 5},
                     {'resourceIdMatches': 'com.cctv.yangshipin.app.androidp:id/btn_.*'},
                     {'resourceId': 'com.cctv.yangshipin.app.androidp:id/vp_guide'},
                     {'textContains': '允许', 'className': 'android.widget.Button'},
                     {'text': '始终允许', 'className': 'android.widget.Button'},
                     {'text': '稍后', 'className': 'android.widget.Button'},
                     {'text': '取消', 'className': 'android.widget.Button'}]
        self.d.app_start(self.pkg_name, stop=True)
        self.timer(delay)
        self._skip_ad()
        time.sleep(1)
        self._skip_homepage_ad()
        if self.d(**{'text': '首页'}).exists(timeout=3):
            return
        count = 1
        while self.d.app_current()['activity'] in app_current_page and count <= repeat:
            logger.debug('App init in %s' % self.d.app_current()['activity'])
            for loc in init_list:
                logger.debug(f'App init in {loc}')
                wait = 1
                if loc.get('wait'):
                    wait = loc.pop('wait')
                _d = self.d(**loc)
                if _d.exists:
                    if loc == {'resourceId': 'com.cctv.yangshipin.app.androidp:id/vp_guide'}:
                        for _ in range(3):
                            # 实验发现，默认的0.9会启动手机的 右滑返回
                            self.d.swipe_ext("left", scale=0.8)
                    else:
                        _d.click()
                time.sleep(wait)
            count += 1
        else:
            if count > repeat:
                raise Exception('init_app fail, exceed max times')
        logger.info('init app success')
    
    def restart_app(self):
        """
        重启App，冷启动
        :return:
        """
        self.d.app_start(self.pkg_name, stop=True)
        logger.debug('restart_app ...')

    def close_app(self):
        """
        杀进程，关闭App
        :return:
        """
        self.d.app_stop(self.pkg_name)
        logger.debug('close_app ...')

    @property
    def cur_activity(self):
        """get current activity

        return (tuple): activity full name and key name
                        such as: ('HomeActivity', ''com.tencent.videolite.android.ui.HomeActivity)
        """
        res = self.d.app_current()['activity']
        return res.split('.')[-1], res

    def ele_exist(self, **kwargs):
        """"""
        res = self.d(**kwargs).exists
        logger.debug('element: %s, exist status is: %s' % (kwargs, res))
        return res

    def ele_text(self, **kwargs):
        """return element's text

        loc (dict): element's locator
        """
        res = self.d(**kwargs).get_text()
        logger.debug('element: %s, text is: %s' % (kwargs, res))
        return res

    def to_click(self, *, wait: int = 10, **loc):
        """click func

        wait: timeout for click
        loc (dict): element's locator
        """
        try:
            self.d(**loc).click(timeout=wait)
            logger.debug(f'to_click {loc}, success')
        except Exception as e:
            logger.error(e)
            self._recovery_mode()
            try:
                self.d(**loc).click(timeout=wait)
            except Exception:
                raise

    def _recovery_mode(self):
        """click's recovery mode, just be used in to_click() !!!"""
        logger.debug('enter recovery_mode ...')
        for name in WHITELIST:
            if self.ele_exist(**name):
                self.d(**name).click()
                logger.debug(f'try to click {name}')
                return

    def wait_for_appear(self, flag: str = '时事'):
        splash_container_loc = {'resourceId': 'com.cctv.yangshipin.app.androidp:id/splash_container'}
        count = 1
        while not self.ele_exist(text=flag) and count <= 10:
            time.sleep(1)
            count += 1
        else:
            if count > 10:
                logger.warning(f'flag: {flag} not appear')
            else:
                if self.ele_exist(**splash_container_loc):
                    count1 = 1
                    while self.ele_exist(**splash_container_loc) and count1 <= 10:
                        time.sleep(1)
                        count1 += 1
                logger.debug(f'flag: {flag} appear')



if __name__ == '__main__':
    boi = BaseOperateIOS('00008020-001D1D900CB9002E')
    print(boi.get_idfv())
    # boa = BaseOperateAND('XPL0219C18016526')
    # ud = UIDriver('ios', '00008020-001D1D900CB9002E')
    pass

