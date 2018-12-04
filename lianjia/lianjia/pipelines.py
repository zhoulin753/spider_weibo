# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class LianjiaPipeline(object):
    def open_spider(self, spider):
        self.db = MySQLdb.connect('127.0.0.1', 'root', 'zl8439736', 'lianjia', charset='utf8')


    def process_item(self, item, spider):
        print('开始{}'.format(item['url']))
        sql = '''insert into house
                (name,houseinfo,area,finish,house_type,floor,address,cost,price,url) 
                  VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}');
              '''.format(item['name'], item['houseinfo'], item['area'],
           item['finish'], item['house_type'], item['floor'],
           item['address'], item['cost'], item['price'], item['url'])
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        print('结束{}'.format(item['url']))
        return item

    def close_spider(self, spider):
        self.db.close()
