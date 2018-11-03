# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# time:2018/10/8

from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
PhantomJS_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'/phantomjs-2.1.1-windows/bin/phantomjs'
from fake_useragent import UserAgent
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
class JavaScriptMiddleware(object):
    page_image = 0

    def process_request(self, request, spider):

        if spider.name == "text":
            # header_dict = dict(DesiredCapabilities.PHANTOMJS)
            # header_dict['phantomjs.page.settings.userAgent'] = \
            #     (
            #         '''
            #         Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36
            #         (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36
            #         ''',
            #     )
            #
            # header_dict["phantomjs.page.settings.loadImages"] = False
            #
            # header_dict["phantomjs.page.customHeaders.Cookie"] = \
            #     '''
            #         SINAGLOBAL=3256254250610.868.1533378616439;
            #         SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWKdSRrZ8dVHJ.AOAIcggUX;
            #         UOR=,,www.baidu.com; YF-Page-G0=1ffbef18656bf02c17e45a764e3d5336;
            #         YF-V5-G0=c072c6ac12a0526ff9af4f0716396363; _s_tentry=-;
            #         Apache=1666052828673.9385.1540703118912;
            #         ULV=1540703118958:18:12:2:1666052828673.9385.1540703118912:1540698454602;
            #         YF-Ugrow-G0=8751d9166f7676afdce9885c6d31cd61;
            #         login_sid_t=92471af86eb7ded87f77b4cef7c8c645;
            #         cross_origin_proto=SSL; wb_view_log=1366*7681;
            #         SUB=_2AkMshe_if8NxqwJRmfgUzGzhaohxyQ7EieKa2R45JRMxHRl-yj83qksAtRB6BwXBDUtMhLS4SEukhk4qD3BoWWck-9P4;
            #         WBStorage=e8781eb7dee3fd7f|undefined
            #     '''
            # header_dict["phantomjs.page.settings.disk-cache"] = True
            # service_args = ['--proxy=127.0.0.1:9999', '--proxy-type=socks5']
            driver = webdriver.PhantomJS(
                                        #desired_capabilities=header_dict,
                                         executable_path=PhantomJS_path,
                                         )  # 指定使用的浏览器
            driver.get(request.url)
            time.sleep(1)
            js = "var q=document.documentElement.scrollTop=1000"
            driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(3)
            body = driver.page_source
            self.page_image += 1
            driver.save_screenshot("weibo{}.png".format(self.page_image))
            print("访问" + request.url)

            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return {}

    def process_response(self, request, response, spider):

        #print(len('https://weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=1760&page=8&lefnav=0&cursor='))
        if len(response.url)<90:
            return response
        else:
            response = self.response_new(response.url)
            return response

    def response_new(self,response_url):
        #这个函数是处理ajxa的数据，拿到的字符串转变成html对象
        import requests
        re = requests.get(response_url)
        re_text = eval(re.text)['data']
        #response=Selector(text=re_text)
        response = HtmlResponse(url=response_url, body=re_text)
        # import json
        # print(json.loads(re))
        return response


class RandomUserAgent(object):

    def __init__(self, crawler):
        super(RandomUserAgent, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANSOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_ua())
        return None

    def process_response(self, request, response, spider):
        return response