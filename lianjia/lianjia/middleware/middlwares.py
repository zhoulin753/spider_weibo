# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# time:2018/11/22
from scrapy.http import HtmlResponse
import time
# from selenium import webdriver
# import os

# PhantomJS_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'/phantomjs-2.1.1-windows/bin/phantomjs.exe'


class JavaScriptMiddleware(object):

    def process_request(self, request, spider):

        if spider.name == "old_house":
            '''
            这个是用phantomjs这个无页面的浏览器来发送我们的请求，但是这个浏览器爬取页面比较慢，需要重新
            择优,当process_request这个方法当返回response对象时，直接跳到process_response方法进行response
            传递
            '''
            driver = webdriver.PhantomJS(executable_path=PhantomJS_path)  # 指定使用的浏览器
            driver.get(request.url)  # 发送url这个请求
            time.sleep(1)
            js = "var q=document.body.scrollTop=10000"
            driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(3)
            body = driver.page_source  # 返回的页面html

            print("访问" + request.url)

            # 封装成response对象，到时我们可以xpath，css，
            return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)
        else:
            return None

    def process_response(self, response, spider):
        print(response.request)
        return response
