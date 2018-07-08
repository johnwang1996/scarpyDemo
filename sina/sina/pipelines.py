# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class SinaPipeline(object):
    def __init__(self):
        self.conn=None
        self.cousor=None

    def open_spider(self,spider):
        #连接
        self.conn=pymysql.connect(host='127.0.0.1',user='root',password='123',
                                  database='fate',port=3306,
                                    charset='utf8')

        #游标
        self.cousor=self.conn.cursor()





    def process_item(self, item, spider):
        sql = "insert into sina(newsTitle,newsUrl,newsTime,content) VALUES (%r,%r,%r,%r)" % \
              (item['newsTitle'], item['newsUrl'], item['newsTime'], item['content'])

        self.cousor.execute(sql)
        self.conn.commit()

        return item

    def close_spider(self,spider):
        self.cousor.close()
        self.conn.close()