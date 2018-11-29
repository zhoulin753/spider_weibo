# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field() #小区名
    houseinfo = scrapy.Field() #户型
    area = scrapy.Field() #面积
    finish= scrapy.Field() #装修
    house_type = scrapy.Field() #朝向
    floor= scrapy.Field() #楼层
    address = scrapy.Field() #地址
    cost = scrapy.Field() #多少钱
    price = scrapy.Field() #单价

