# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
import os
from lianjia.items import LianjiaItem
import json
from scrapy.http import HtmlResponse
from scrapy.http import Request

PhantomJS_path = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))) + r'/phantomjs-2.1.1-windows/bin/phantomjs.exe'

add_url = {}

class OldHouseSpider(CrawlSpider):
    name = 'old_house'
    # allowed_domains = ['sh.lianjia.com/ershoufang/']
    start_urls = ['https://sh.lianjia.com/ershoufang/pudong/',
                  'https://sh.lianjia.com/ershoufang/minhang/',
                  'https://sh.lianjia.com/ershoufang/baoshan/',
                  'https://sh.lianjia.com/ershoufang/xuhui/',
                  'https://sh.lianjia.com/ershoufang/putuo/',
                  'https://sh.lianjia.com/ershoufang/yangpu/',
                  'https://sh.lianjia.com/ershoufang/changning/',
                  'https://sh.lianjia.com/ershoufang/songjiang/',
                  'https://sh.lianjia.com/ershoufang/jiading/',
                  'https://sh.lianjia.com/ershoufang/huangpu/',
                  'https://sh.lianjia.com/ershoufang/jingan/',
                  'https://sh.lianjia.com/ershoufang/zhabei/',
                  'https://sh.lianjia.com/ershoufang/hongkou/',
                  'https://sh.lianjia.com/ershoufang/qingpu/',
                  'https://sh.lianjia.com/ershoufang/fengxian/',
                  'https://sh.lianjia.com/ershoufang/jinshan/',
                  'https://sh.lianjia.com/ershoufang/chongming/',
                  'https://sh.lianjia.com/ershoufang/shanghaizhoubian/']
    driver = webdriver.PhantomJS(executable_path=PhantomJS_path)

    rules = (
        Rule(
            LinkExtractor(
                # allow='/ershoufang\w+/',
                restrict_xpaths=r'//div[@data-role="ershoufang"]/div[2]/a'
            ),
            callback='parse_item',
            follow=True),

    )


    def parse_item(self, response):
        item = LianjiaItem()
        page = self.get_page(response)
        new_page = 1
        while add_url[response.url.split('/')[4]] >= new_page:
            response_or_resquest = self.send_requset(response, new_page)
            print(add_url)
            if isinstance(response_or_resquest, HtmlResponse):
                print('开始解析', response.url)
                new_page += 1
            elif isinstance(response_or_resquest, Request):
                print('request:', 'ok', response.url)
                yield response_or_resquest
                new_page += 1
            else:
                print('结束：', response.url)
                break
    def get_page(self, response):
        url_list = response.url.split('/')
        if not url_list[5]:
            page = json.loads(response.xpath('//div[@comp-module="page"]/@page-data')[0].extract())['totalPage']
            add_url[url_list[4]] = int(page)
            print('get_page运行结束', add_url)


    def send_requset(self, response, new_page):
        url_list = response.url.split('/')
        if url_list[5]=='':
            print('url_list[5]', url_list)
            return Request(response.url + 'pg' + str(new_page) + '/', callback=self.parse_item)
        else:
            page = int(url_list[5][3:])
            if add_url[url_list[4]] >= page and url_list[6]=='' and len(url_list) > 7:
                return Request(response.url + 'pg' + str(new_page) + '/', callback=self.parse_item)
            else:
                return None
