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

class FoxNewsSpider(scrapy.Spider):
    name = "foxnews"

    def start_requests(self):
        urls = []
        urls += open('links_foxnews.txt', 'r').read().split('\n')
        for url in set(urls):
          if url != '':
            yield scrapy.Request(url = url, callback = self.parse, meta = {'dont_merge_cookies': True}, headers = {"User-agent": "Mozilla/5.0"})


    def parse(self, response):

        try:
            title = response.selector.xpath('//h1[@class = "headline head1"]/text()')[0].extract()
        except:
            title = ''

        try:
            body = response.selector.xpath('//div[@class = "article-body"]//p//text()').extract()
            body = '\n'.join(body)
        except:
            body = ''

        try:
            date = response.selector.xpath('//time/@data-time-published')[0].extract()
            date = date.split('T')[0]
        except:
            date = ''

        try:
            section = response.url.split('/')[3]
        except:
            section = ''
        
        item = Item()
        item['title'] = title
	item['section'] = section
        item['date'] = date
        item['body'] = body

        item['newspaper'] = u'Fox News'
	item['url'] = response.url

        return item
