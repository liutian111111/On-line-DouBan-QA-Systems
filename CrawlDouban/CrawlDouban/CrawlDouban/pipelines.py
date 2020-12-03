# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CrawldoubanPipeline(object):
    
    def open_spider(self,spider):
        self.data_file=codecs.open('./CrawlDouban/Data/douban_info.json','a+','utf-8')
    
    def process_item(self,item,spider):
        if item is not None:
            json_str=json.dumps(dict(item))+'\n'
            self.data_file.write(json_str)
            self.data_file.flush()
            return item

