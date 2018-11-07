#！/usr/bin/env python
# -*- coding:utf-8 -*-
#time:2018/11/5
import requests
from scrapy.selector import Selector
'''112.64.60.115'''
class GetIp(object):

    def __init__(self):
        self.xici = 'http://www.xicidaili.com/wn/'
        self.page = 1
    def send_requset(self):
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }


        proxies = {'http':'http://adslsdfsdfspider01.wsdfeb.zwsdf.tsdfed:9090'}
        # proxies = {'http': '125.125.215.174:53128'}

        response = requests.post('http://icanhazip.com/', headers=header, proxies = proxies)
        print(response.text)
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

        self.page += 1
        self.again_new_request()
        return add


    def again_new_request(self):
        if self.page == 2:
            self.xici = self.xici +str(self.page)
        elif self.page == 10:
            exit()
        elif self.page > 2:
            self.xici = self.xici[:-1] + str(self.page)

        print(self.xici)
        self.send_requset()


a = GetIp()
a.send_requset()