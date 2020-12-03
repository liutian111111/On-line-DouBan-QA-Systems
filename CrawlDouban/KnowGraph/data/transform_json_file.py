# -*- coding: UTF-8 -*-
import json
import codecs

with codecs.open('./douban_info.json','r+','utf-8') as fin,\
    codecs.open('./douban_info_out.json','w+','utf-8') as fout,\
    codecs.open('./douban_info_GPU1.json','r+','utf-8') as fin2:
    lines=fin.readlines()
    for line in lines:
        json_dict=json.loads(line.strip(),'utf-8')
        json_str=json.dumps(json_dict,ensure_ascii=False,encoding='utf-8')
        fout.write(json_str+'\n')
    lines=fin2.readlines()
    for line in lines:
        json_dict=json.loads(line.strip(),'utf-8')
        json_str=json.dumps(json_dict,ensure_ascii=False,encoding='utf-8')
        fout.write(json_str+'\n')

