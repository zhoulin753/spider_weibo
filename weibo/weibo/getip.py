#！/usr/bin/env python
# -*- coding:utf-8 -*-
#time:2018/11/5
import requests
from scrapy.selector import Selector

class GetIp(object):

    def __init__(self):
        self.xici = 'http://www.xicidaili.com/wn/'

    def send_requset(self):
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        response = requests.get(self.xici, headers=header)

        response = Selector(text=response.text)

        return response

    def get_ip(self):
        response = self.send_requset()
        hide = response.xpath('//tr[@class]/tb[5]')
        ip = hide.xpath('../tr[@class]/tb[2]')
        print(response.body)
a = GetIp()
a.get_ip()