#coding=utf-8
import re

query_items=[
    '书名 (.+)',
    '作者 (.+)',
    '评分 (.+)',
    '出版社 (.+)'
]

if __name__=='__main__':
    question='书名 雨水'
    for q_i in query_items:
        ans=re.findall(q_i,question)
        print(ans)