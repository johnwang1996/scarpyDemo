# -*- coding: utf-8 -*-
import scrapy
import requests
import lxml
from lxml import etree
from sina import items


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MysinaSpider(scrapy.Spider):
    name = 'mysina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_2.shtml']
    #规则
    #allow=(正则)允许,deny=(正则）不允许
    #callback=回调
    #follow=跟随如果为True
    rules=[Rule(LinkExtractor(allow=("index_(\d+).shtml")),callback="getparse",follow=True)]
    def parse(self, response):
        print(response.url)
        newsList=response.xpath('//ul[@class="list_009"]/li')

        for news in newsList:
            item=items.SinaItem()

            #标题
            #extract()提取真实内容
            newsTitle=news.xpath('./a/text()')[0].extract()
            #url
            newsUrl=news.xpath('./a/@href')[0].extract()
            #新闻事件
            newsTime=news.xpath('./span/text()')[0].extract()

            #正文
            content=self.getContent(newsUrl)

            item["newsTitle"]=newsTitle
            item["newsUrl"]=newsUrl
            item["newsTime"]=newsTime
            item["content"]=content

            yield

    def getContent(self,url):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

            response=requests.get(url,headers=headers).content.decode('utf-8','ignore')
            mytree=lxml.etree.HTML(response)
            contentList=mytree.xpath('//div[@id="article"]//text()')
            content=''
            for c in contentList:
                # print(c)
                content +=c.strip()

            return
