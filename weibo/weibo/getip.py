#！/usr/bin/env python
# -*- coding:utf-8 -*-
#time:2018/11/5
import requests
from scrapy.selector import Selector

class GetIp(object):

    def __init__(self):
        self.xici = 'http://www.xicidaili.com/wn/'
        self.page = 0

    def send_requset(self):
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

        response = requests.get(self.xici, headers=header)

        response = Selector(text=response.text)

        self.get_ip(response)


    def get_ip(self, response):

        tr_every = response.xpath('//tr')[1:]
        add = []
        # print(response)
        for i in tr_every:
            if i.xpath('td[5]/text()').extract()[0] == '高匿' and \
                    eval(i.xpath('td[7]/div/@title').extract()[0][:-1]) < 1.000 and \
                    eval(i.xpath('td[8]/div/@title').extract()[0][:-1]) < 1.000 and \
                    i.xpath('td[9]/text()').extract()[0][-1]=='天' and \
                    eval(i.xpath('td[9]/text()').extract()[0][:-1])>5:

                ip = i.xpath('td[2]/text()').extract_first()
                port = i.xpath('td[3]/text()').extract_first()
                add.append((ip, port))
        print(add)
        for page in :
            print(page)
            self.page += 1
            self.again_new_request()

        return add


    def again_new_request(self):
        self.xici = self.xici+ str(self.page)
        print(self.xici)
        self.send_requset()


a = GetIp()
a.send_requset()