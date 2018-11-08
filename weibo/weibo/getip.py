# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# time:2018/11/5
import requests
from scrapy.selector import Selector
from fake_useragent import UserAgent
import time
import sys
import base64
'''112.64.60.115'''
# def base_code(username, password):
#     str = '%s:%s' % (username, password)
#     encodestr = base64.b64encode(str.encode('utf-8'))
#     return '%s' % encodestr.decode()

class GetIp(object):
    ua = UserAgent()
    def __init__(self):
        self.xici = 'http://www.xicidaili.com/wn/'
        self.page = 1

    def send_requset(self):
        header = {
            'User-Agent': self.ua.random ,
            # 'Accept - Encoding': 'gzip, deflate',
            # 'Accept-Language' :'zh-CN,zh;q=0.9',
            # 'Cache-Control':'max-age=0',
            # 'Host' : 'selenium.10932.n7.nabble.com',
            # 'If-Modified-Since' : 'Tue, 06 Nov 2018 22:56:30 GMT',
            # 'If-None-Match':'13:10932~2:10932:59623~1:10932:8051~1:10932:2',
            # 'Upgrade-Insecure-Requests':'1',
            # 'Content - Length': '41',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Content - Type': 'application / json;charset = UTF - 8',
            # 'Connection': 'keep - alive'

        }
        proxy_dict = {
            "https": "61.133.245.70:35652",
        }

        # username = "1281263636@qq.com"  # 您的用户名
        # password = "Zl8439736"  # 您的密码
        # proxy_ip = "113.237.186.10"  # 代理ip，通过http://h.wandouip.com/get获得
        # proxy_port = "766"  # 代理端口号
        # header = {
        #     'Proxy-Authorization': 'Basic %s' % (base_code(username, password))
        # }
        # proxy_dict = {
        #     'http': 'http://%s:%s' % (proxy_ip, proxy_port),
        #     'https': 'https://%s:%s' % (proxy_ip, proxy_port)
        # }

        try:
            response = requests.get(self.xici, headers=header)
            # print(response.text)
            time.sleep(3)
            response = Selector(text=response.text)
            self.get_ip(response)
        except requests.exceptions.ProxyError:
            print('访问失败')
        else:
            a.send_requset()

    def get_ip(self, response):
        tr_every = response.xpath('//tr')[1:]
        add = []
        for i in tr_every:
            if i.xpath('td[5]/text()').extract()[0] == '高匿' and \
                    eval(i.xpath('td[7]/div/@title').extract()[0][:-1]) < 1.000 and \
                    eval(i.xpath('td[8]/div/@title').extract()[0][:-1]) < 1.000 and \
                    i.xpath('td[9]/text()').extract()[0][-1] == '天' and \
                    eval(i.xpath('td[9]/text()').extract()[0][:-1]) > 5:
                ip = i.xpath('td[2]/text()').extract_first()
                port = i.xpath('td[3]/text()').extract_first()
                add.append((ip, port))

        self.write_ip(add)
        self.page += 1
        self.again_new_request()


    def again_new_request(self):
        if self.page == 2:
            self.xici = self.xici + str(self.page)
        elif self.page == 10:
            sys.exit()
        elif self.page > 2:
            self.xici = self.xici[:-1] + str(self.page)
        print(self.xici)
        self.send_requset()

    def write_ip(self, add):
        for index, adder in enumerate(add):
            if self.page == 1 and index == 0:
                write_str = 'w'
            else:
                write_str = 'a+'
            ip, port = adder
            with open('add.text', write_str) as f:
                f.write(ip +':'+port + '\n')
a = GetIp()
a.send_requset()
