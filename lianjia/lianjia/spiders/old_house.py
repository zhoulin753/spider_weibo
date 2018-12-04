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

                restrict_xpaths=r'//div[@data-role="ershoufang"]/div[2]/a'
            ),
            callback='parse_item',
            follow=True),

    )

    def parse_item(self, response):
        item = LianjiaItem()
        self.get_page(response)
        if response.url.split('/')[5] == '':
            visited_page = 1
            new_page = 1
        else:
            visited_page = int(response.url.split('/')[5][2:])
            new_page = visited_page + 1
        for info in self.analysis_response(response, item):
            yield info

        if add_url[response.url.split('/')[4]] >= new_page:
            response_or_resquest = self.send_requset(response, visited_page)
            if isinstance(response_or_resquest, HtmlResponse):
                if response.url not in self.start_urls:
                    yield Request(response.url + 'pg{}'.format(new_page + 1) + '/',
                                  callback=self.parse_item)
            elif isinstance(response_or_resquest, Request):
                yield response_or_resquest

    def get_page(self, response):
        url_list = response.url.split('/')
        if url_list[5] == '':
            try:
                page = json.loads(response.xpath('//div[@comp-module="page"]/@page-data')[0].extract())['totalPage']
                add_url[url_list[4]] = int(page)

            except:
                add_url[url_list[4]] = 1

    def send_requset(self, response, visited_page):
        url_list = response.url.split('/')
        if url_list[5] == '':
            return response
        elif url_list[5] != '':
            return Request(response.url.replace('pg{}'.format(visited_page), 'pg{}'.format(visited_page + 1)),
                           callback=self.parse_item)

    def analysis_response(self, response, item):
        page_information_list = response.xpath('//li[@class="clear LOGCLICKDATA"]/div[@class="info clear"]')
        # print(page_information_list)
        for i in page_information_list:
            item['title'] = i.xpath('div[@class="title"]/a/text()')[0].extract().strip()
            item['name'] = i.xpath('div[@class="address"]/div[@class="houseInfo"]/a/text()')[0].extract().strip()
            item['houseinfo'] = \
                i.xpath('div[@class="address"]/div[@class="houseInfo"]/text()')[0].extract().split('|')[1].strip()
            item['area'] = i.xpath('div[@class="address"]/div[@class="houseInfo"]/text()')[0].extract().split('|')[2].strip()
            item['finish'] = i.xpath('div[@class="address"]/div[@class="houseInfo"]/text()')[0].extract().split('|')[4].strip()
            item['house_type'] = \
                i.xpath('div[@class="address"]/div[@class="houseInfo"]/text()')[0].extract().split('|')[3].strip()
            item['floor'] = i.xpath('div[@class="flood"]/div[@class="positionInfo"]/text()')[0].extract().strip()
            item['address'] = i.xpath('div[@class="flood"]/div[@class="positionInfo"]/a/text()')[0].extract().strip()
            item['cost'] = i.xpath('div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()')[0].extract().strip()
            item['price'] = i.xpath('div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()')[0].extract()[2:-4].strip()
            item['url'] = response.url
            yield item

