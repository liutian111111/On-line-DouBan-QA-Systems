# -*- coding: utf-8 -*-
from xlrd import open_workbook
import codecs
import json
import os

book_list_file=[filename for filename in os.listdir('./') if filename.startswith('book')]
for book_table in book_list_file:
    with open_workbook(book_table,'r+') as fin, \
        codecs.open('book.json','a+','utf-8') as fout:
        table=fin.sheet_by_index(0)
        category=book_table.split('-')[1]
        for row in range(1,table.nrows):
            row_value=table.row_values(row)
            item={}
            item['name']=row_value[1]
            try: 
                if u'作者/译者：' in row_value[4]:
                    author=row_value[4].replace(u'作者/译者：','') 
                    item['author']=author
                else:
                    item['author']=row_value[4]
            except Exception:
                item['author']=None
            item['category']=category
            try:
                if u'出版信息：' in row_value[5]:
                    info=row_value[5].replace(u'出版信息：','')
                else:
                    info=row_value[5]
                publisher,pubtime,prize=info.split('/')
            except Exception:
                publisher=None
                pubtime=None
                prize=None
            item['publisher']=publisher
            item['pubtime']=pubtime
            item['prize']=prize
            item['rating']=row_value[2]
            item['review_num']=row_value[3]
            item['content']=None
            try:
                json_str=json.dumps(item,ensure_ascii=False, encoding='utf-8')
            except Exception:
                json_str=json.dumps(item)
            fout.write(json_str+'\n')
            