# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# time:2018/10/8

from selenium import webdriver

import time
import os

PhantomJS_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'/phantomjs-2.1.1-windows/bin/phantomjs'
from fake_useragent import UserAgent

from scrapy.http import HtmlResponse
'''
这个文件是专门处理我们的request和response的，当有新的url需要请求时，都会来到这个中间件，
当有新的response时，都会来到这个中间件，来处理，所以我们可以在请求要发送出去之前，来到这处理
同理response也是一样的！
注意：在下载中间件中我们有三个固定的方法：process_request，process_response,process
'''
class JavaScriptMiddleware(object):
    # page_image = 0

    def process_request(self, request, spider):

        if spider.name == "text":
            '''
            这个是用phantomjs这个无页面的浏览器来发送我们的请求，
            '''
            driver = webdriver.PhantomJS(executable_path=PhantomJS_path)  # 指定使用的浏览器
            driver.get(request.url)
            time.sleep(1)
            js = "var q=document.documentElement.scrollTop=1000"
            driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(3)
            body = driver.page_source
            print("访问" + request.url)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return {}

    def process_response(self, request, response, spider):

        if len(response.url)<90:
            return response
        else:
            response = self.response_new(response.url,request)
            return response

    def response_new(self,response_url,request):
        #这个函数是处理ajxa的数据，拿到的字符串转变成html对象
        import requests
        re = requests.get(response_url)
        re_text = eval(re.text)['data']
        #response=Selector(text=re_text)
        b = '\\'

        print('find:',re_text.find(b))
        if re_text.find(b) > 0:
            new_re_text_list = re_text.split(b)

            re_text = ''.join(new_re_text_list)
        response = HtmlResponse(url=response_url, body=re_text, encoding='utf8', request=request)

        return response


class RandomUserAgent(object):

    def __init__(self, crawler):
        super(RandomUserAgent, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANSOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        #当创建这个方法时，先运行这个类方法，之后将运行这个__init__这个方法，将这个cls==》self
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_ua())
        return None

    def process_response(self, request, response, spider):
        return response