# -*- coding: utf-8 -*-
import scrapy

class Item(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    body = scrapy.Field()
    prefix = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    newspaper = scrapy.Field()
    section = scrapy.Field()
    tag = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()

class USATodaySpider(scrapy.Spider):
    name = "usatoday"

    def start_requests(self):
        urls = []
        urls += open('links_usatoday.txt', 'r').read().split('\n')
        for url in set(urls):
          if url != '':
            yield scrapy.Request(url = url, callback = self.parse, meta = {'dont_merge_cookies': True}, headers = {"User-agent": "Mozilla/5.0"})


    def parse(self, response):

        try:
            title = response.selector.xpath('//h1[@itemprop = "headline"]/text()')[0].extract()
        except:
            title = ''

        try:
            body = response.selector.xpath('//div[@itemprop = "mainEntity articleBody"]//p//text()').extract()
            body = '\n'.join(body)
        except:
            body = ''
 
        try:
            date = response.selector.xpath('//span[@class = "asset-metabar-time asset-metabar-item nobyline"]/text()')[0].extract()
            date = date.split('ET')[1].split(' ')
            date = ' '.join([date[1], date[2], date[3]])
            date = date.replace('\n','')
        except:
            date = ''

        item = Item()
        item['title'] = title
	item['section'] = ''
        item['date'] = date
        item['body'] = body

        item['newspaper'] = u'USA Today'
	item['url'] = response.url

        return item
