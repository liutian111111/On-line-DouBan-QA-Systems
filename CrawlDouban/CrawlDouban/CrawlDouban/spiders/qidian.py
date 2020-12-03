# -*- coding: utf-8 -*-
import scrapy
import json
import codecs
from scrapy import Request
from CrawlDouban.items import *


class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['http://qidian.com/',
    'https://www.qidian.com/search?kw=']
    json_file='./CrawlDouban/Data/book.json'

    def open_json_file(self):
        with codecs.open(self.json_file,'r+','utf-8') as fin:
            lines=fin.readlines()
            for line in lines:
                book_dict=json.loads(line)
                yield book_dict

    def parse(self, response, book_info):
        content=response.selector.xpath('//div[@class="book-mid-info"]/p[@class="intro"]//text()').extract()
        item=CrawldoubanItem()
        item['category']=book_info['category']
        item['name']=book_info['name']
        item['author']=book_info['author']
        item['publisher']=book_info['publisher']
        item['pubtime']=book_info['pubtime']
        item['prize']=book_info['prize']
        item['rating']=book_info['rating']
        item['review_num']=book_info['review_num']
        item['content']=content[0]
        yield item

    def start_requests(self):
        book_list=self.open_json_file()
        for book_info in book_list:
            yield Request(self.start_urls[1]+book_info['name'],callback=lambda response,book_info=book_info:self.parse(response,book_info))

