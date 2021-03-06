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

class NYTimesSpider(scrapy.Spider):
    name = "nytimes"

    def start_requests(self):
        urls = []
        urls += open('links_nytimes.txt', 'r').read().split('\n')
        for url in set(urls):
          if url != '':
            yield scrapy.Request(url = url, callback = self.parse, meta = {'dont_merge_cookies': True}, headers = {"User-agent": "Mozilla/5.0"})


    def parse(self, response):

        try:
            title = response.selector.xpath('//h1[@itemprop = "headline"]/text()')[0].extract()
        except:
            title = ''

        try:
            body = response.selector.xpath('//p[@class = "story-body-text story-content"]//text()').extract()
            body = '\n'.join(body)
        except:
            body = ''

        try:
            date = response.selector.xpath('//time[@class = "dateline"]/text()')[0].extract()
        except:
            date = ''

        try:
            section = response.selector.xpath('//span[@class = "kicker-label"]//text()')[0].extract()
        except:
            section = ''
        
        item = Item()
        item['title'] = title
	item['section'] = section
        item['date'] = date
        item['body'] = body

        item['newspaper'] = u'New York Times'
	item['url'] = response.url

        return item
