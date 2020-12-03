# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from CrawlDouban.items import *


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/',
    'https://book.douban.com/tag/?view=type&icn=index-sorttags-all',
    'https://book.douban.com/tag/*?start=#&type=T']
    #book_term=range(0,100,20)

    def parse_book(self,response,category):
        name=response.selector.xpath('//div[@id="wrapper"]/h1/span[@property="v:itemreviewed"]/text()').extract()
        author=response.selector.xpath('//div[@class="subject clearfix"]/div[@id="info"]/span/a/text()').extract()
        publisher=response.selector.xpath(u'//div[@class="subject clearfix"]/div[@id="info"]/span[./text()="出版社:"]/following::text()[1]').extract()
        pubtime=response.selector.xpath(u'//div[@class="subject clearfix"]/div[@id="info"]/span[./text()="出版年:"]/following::text()[1]').extract()
        prize=response.selector.xpath(u'//div[@class="subject clearfix"]/div[@id="info"]/span[./text()="定价:"]/following::text()[1]').extract()
        rating=response.selector.xpath('//div[@class="rating_self clearfix"]/strong/text()').extract()
        review_num=response.selector.xpath('//div[@class="rating_sum"]/span/a/span/text()').extract()
        content=response.selector.xpath('//div[@class="intro"]/p/text()').extract()[0]
        item=CrawldoubanItem()
        item['category']=category
        item['name']=name[0]
        item['author']=author[0]
        item['publisher']=publisher[0]
        item['pubtime']=pubtime[0]
        item['prize']=prize[0]
        item['rating']=rating[0]
        item['review_num']=review_num[0]
        item['content']=content
        #print name,category,author,publisher,pubtime,prize,rating,review_num
        #print content
        yield item


    def parse_page(self,response,category):
        book_link=response.selector.xpath('//li[@class="subject-item"]/div[@class="pic"]/a/@href').extract()
        #print 'book_link:',len(book_link)
        for link in book_link:
            #print link
            yield Request(link,callback=lambda response, category=category:self.parse_book(response,category),headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"})
    
    def parse(self, response):
        category_list=response.selector.xpath('//table[@class="tagCol"]/tbody/tr/td/a/text()').extract()
        for it in category_list:
            for tm in range(0,1000,20):
                #print(self.start_urls[2].replace('*',it).replace('#',str(tm)))
                yield Request(self.start_urls[2].replace('*',it).replace('#',str(tm)),callback=lambda response, category=it: self.parse_page(response,category),headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"})
    
    def start_requests(self):
        yield Request(self.start_urls[1],callback=lambda response: self.parse(response),headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"})
