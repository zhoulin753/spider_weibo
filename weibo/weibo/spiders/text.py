# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from weibo.items import WeiboItem
import json
'''https://passport.weibo.com/visitor/visitor?entry=miniblog&
a=enter&url=https%3A%2F%2Fweibo.com%2Fttarticle%2Fp%2Fshow%3Fid%3D2309404298589458312259&domain=.weibo.com&ua=php-sso_sdk_clien
t-0.6.28&_rand=1540348813.0018'''
'''
 https://passport.weibo.com/visitor/visitor?entry=miniblog&
 a=enter&url=https%3A%2F%2Fweibo.com%2Fttarticle%2Fp%2Fshow%3Fid%3D2309404298262772365509&domain=.weibo.com&ua=php-sso_sdk_clien
 t-0.6.28&_rand=1540364023.6962
'''
def append_url(list):
    page = 3

    for i in range(10):
        url = r'https://weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=1760&page={}&lefnav=0&cursor='.format(page)
        page+=1
        list.append(url)
    return list

class TextSpider(CrawlSpider):
    name = 'text'
    allowed_domains = ['weibo.com']

    start_urls = [
        'https://weibo.com/?category=12',
        'https://weibo.com/?category=7',
        'https://weibo.com/?category=10018',
        'https://weibo.com/?category=10007',
        'https://weibo.com/?category=1760',
        'https://weibo.com/?category=novelty',
        'https://weibo.com/?category=99991',



    ]
    start_urls=append_url(start_urls)

    rules = (
        Rule(LinkExtractor(
            #allow=r'id=\d+',
            restrict_xpaths='//h3[@class="list_title_b"]/a | //meta'),
            callback='parse_item',
            follow=True,

        ),
    )

    def parse_item(self, response):

        print('1',response)
        title = response.xpath(
            r'//div[@node-type="articleTitle"]/text()')[0].extract()
        print('1',title)
        author = response.xpath(r"//em[@class='W_autocut']/text()")[0].extract()
        time_list = response.xpath(r'//span[@class="time"]/text()')[0].extract().split(' ')
        time = time_list[1] + ' ' + time_list[2]
        if not title:
            print('2',response)
            response = response.xpath('//body')
            title = response.xpath(
                r'//div[@node-type="articleTitle"]/text()')[0].extract()
            print('2',title)
            author = response.xpath(r"//em[@class='W_autocut']/text()")[0].extract()
            time_list = response.xpath(r'//span[@class="time"]/text()')[0].extract().split(' ')
            time = time_list[1] + ' ' + time_list[2]

            # title='空'
            # author='空'
            # time_list=['空']
            # time='0-0-0-0-0-0-0-0'

        xpath_list = [
            r'//p[@align="justify"]/text()',
            r'//font[@color="#333333"]/text()',
            r'//div[@class="WB_artical_del"]/p[@class="text"]/text()',
            r'//div[@node-type="contentBody"]/p/text()'
        ]
        for i in xpath_list:
            article_list = response.xpath(i)
            #print('i:',i)
            #print('article_list_in:',article_list)
            if article_list != []:
                #print(article_list)
                break

        article = ''
        for i in article_list:
            article += i.extract()
        item = WeiboItem()
        item['title'] = title
        item['author'] = author
        item['article'] = article
        item['time'] = time
        print('parse解决了', article)
        yield item


