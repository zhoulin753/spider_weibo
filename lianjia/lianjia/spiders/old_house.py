# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
import os
PhantomJS_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'/phantomjs-2.1.1-windows/bin/phantomjs.exe'

class OldHouseSpider(CrawlSpider):
    name = 'old_house'
    allowed_domains = ['https://sh.lianjia.com/ershoufang/']
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
                 allow='/ershoufang\w+/',
                restrict_xpaths=r'//div[@data-role="ershoufang"]/div[2]/a'
                ),
            callback='self.parse_item',
            follow=True),
    )

    def parse_item(self, response):
        print('111111111')
        print(response.url)
        # i = {}
        # #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # #i['name'] = response.xpath('//div[@id="name"]').extract()
        # #i['description'] = response.xpath('//div[@id="description"]').extract()
        # yield i
        pass