#！/usr/bin/env python
# -*- coding:utf-8 -*-
#time:2018/11/5
import requests
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
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
        tr_every = response.xpath('//tr')[1:]
        # print(response)
        for   i in tr_every:
            print(i.xpath('//tr[1]/td/text()').extract())
            if i.xpath('//td[4]/text()').extract() == '高匿':

                print('高匿:',i.xpath('//td[2]/text()').extract())
a = GetIp()
a.get_ip()