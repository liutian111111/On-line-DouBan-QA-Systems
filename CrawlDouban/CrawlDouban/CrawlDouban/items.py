# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawldoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category=scrapy.Field()
    name=scrapy.Field()
    author=scrapy.Field()
    publisher=scrapy.Field()
    rating=scrapy.Field()
    pubtime=scrapy.Field()
    prize=scrapy.Field()
    content=scrapy.Field()
    review_num=scrapy.Field()



