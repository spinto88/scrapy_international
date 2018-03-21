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

class HuffPostSpider(scrapy.Spider):
    name = "huffpost"

    def start_requests(self):
        urls = []
        urls += open('links_huff.txt', 'r').read().split('\n')
        for url in set(urls):
          if url != '':
            yield scrapy.Request(url = url, callback = self.parse, meta = {'dont_merge_cookies': True},headers = {'User-agent':'Mozilla/5.0'})


    def parse(self, response):

        try:
            title = response.selector.xpath('//h1[@class = "headline__title"]/text()')[0].extract()
        except:
            title = ''

        try:
            body = response.selector.xpath('//div[@class = "entry__text js-entry-text bn-entry-text yr-entry-text"]//p//text()').extract()
            body = '\n'.join(body)
        except:
            body = ''

        try:
            date = response.selector.xpath('//span[@class="timestamp__date--published"]//text()')[0].extract()
            date = date.split(' ')[0].split('/')
            date = '-'.join([date[1], date[0], date[2]])
        except:
            date = ''

        try:
            section = response.selector.xpath('//span[@class = "entry-eyebrow"]//a//text()')[0].extract()
            section = section.replace('\n','')
        except:
            section = ''
        
        item = Item()
        item['title'] = title
	item['section'] = section
        item['date'] = date
        item['body'] = body

        item['newspaper'] = u'Huffington Post'
	item['url'] = response.url

        return item
