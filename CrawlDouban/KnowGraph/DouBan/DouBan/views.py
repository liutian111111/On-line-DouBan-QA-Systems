# -*- coding: UTF-8 -*-
from django.shortcuts import render
from py2neo import Node, Relationship, Graph, NodeMatcher
from django.views.decorators import csrf
import re
from LAC import LAC
lac=LAC(mode='lac')
#from stanfordcorenlp import StanfordCoreNLP
#nlp_zh = StanfordCoreNLP(r'/home/tianyi/Program/Law-predict/corenlp/stanford-corenlp-4.1.0/', lang='zh')

douban_graph= Graph(
    "http://localhost:7474", 
    username="neo4j", 
    password="neo4j"
)

def rules(question):
    query_items=[
    u'书名 (.+)',
    u'作者 (.+)'
    ]

    for i,q_i in enumerate(query_items):
        #print(i,q_i,question)
        ans=re.findall(q_i,question)
        if len(ans)!=0:
            if i==0:
                #print(ans[0])
                return 'BOOK', ans[0]
            if i==1:
                #print(ans[0])
                return 'AUTHOR', ans[0]
    return None

def rulesForEntity(question):
    rules_for_book=['(.*?)[的是]*(哪个人写|作者|谁写)',
    '(.*?)[的]*(讲|主要内容|内容|主要讲|简介)',
    '(.*?)[的是谁什么哪段时间年代]*(出版|发布|发行)',
    '(.*?)[的是]*(多少钱|价格|价钱|价值|值|定价)',
    '(.*?)[的]*(评分|评价)']
    rules_for_author=['(.*?)[的]*(作品|写|创作|著作)']
    entities_book=[]
    entities_author=[]
    for rule in rules_for_book:
        res=re.findall(rule,question)
        if len(res)!=0:
            #print(type(res[0][0]))
            entities_book.append(res[0][0])
            break
    res=re.findall(rules_for_author[0],question)
    if len(res)!=0:
        #print(type(res[0][0]))
        entities_author.append(res[0][0])
    return entities_book,entities_author

def getNameEntity(question):
    question_type={'author':['写','创作','作者'],'time':['年','时间','年份'],'prize':['价钱','价格','钱'],'content':['内容','简介','讲了'],'publisher':['出版','发行','出版社','发行商'],'rating':['评分','评价'],'book':['作品','哪些书','书','著作']}
    question_keys=['author','time','prize','content','publisher','rating','book']
    doc=lac.run(question.decode('utf-8'))
    print(doc)
    entities_book=[doc[0][i].encode('utf-8') for i in range(len(doc[1])) if doc[1][i]=='nw' or doc[1][i]=='nz']
    entities_author=[doc[0][i].encode('utf-8') for i in range(len(doc[1])) if doc[1][i]=='PER']
    if len(entities_book)==0 or len(entities_author)==0:
        book,author=rulesForEntity(question)
        if len(entities_book)==0:
            entities_book=book
        if len(entities_author)==0:
            entities_author=author
    if len(entities_book)!=0 and entities_book[0] in question:
        question=question.replace(entities_book[0],'')
    if len(entities_author)!=0 and entities_author[0] in question:
        question=question.replace(entities_author[0],'')
    if len(entities_book)==0 and len(entities_author)==0:
        return None
    else:
        for k in question_keys:
            for k_word in question_type[k]:
                if k!='book':
                    if k_word in question and len(entities_book)!=0:
                        #print(k)
                        #print(k_word)
                        return k,entities_book[0]
                else:
                    if k_word in question and len(entities_author)!=0:
                        #print(k)
                        #print(k_word)
                        return k,entities_author[0]
        return None

def searchKnowGraph(ID_NAME=None,NAME=None,Q_TYPE=None,QUERY=None):
    matcher=NodeMatcher(douban_graph)
    try:
        item_search=matcher.match(ID_NAME,name=NAME).all()
        tmp_search=item_search[0]
        tmp_cont_len=len(dict(tmp_search)['content'])
        for item in item_search:
            if len(dict(item)['content'])>tmp_cont_len:
                tmp_cont_len=len(dict(item)['content'])
                tmp_search=item
        item_search=tmp_search
        print('name:',NAME)
        if ID_NAME=='BOOK' and item_search is not None:
            item_search_dict=dict(item_search)
            author_name=douban_graph.match_one((item_search,), r_type="book_author_is").end_node['name']
            rating_score=douban_graph.match_one((item_search,),r_type="book_rating_is").end_node['score']
            category=douban_graph.match_one((item_search,),r_type="book_category_is").end_node['name'].replace('.xlsx','')
            publisher=douban_graph.match_one((item_search,),r_type="book_publisher_is").end_node['name']
            if Q_TYPE is None:
                result_dict={'main':QUERY,\
                    'info':item_search_dict['name']+' '+author_name+' '+category+' '+rating_score.encode('utf-8')+' '+publisher+' '+item_search_dict['publish_time'].encode('utf-8')+'\n'+item_search_dict['content']}
                result_str=item_search_dict['name']+' '+author_name+' '+category+' '+rating_score.encode('utf-8')+' '+publisher+' '+item_search_dict['publish_time'].encode('utf-8')+'\n'+item_search_dict['content']
                print(result_str)
            else:
                if Q_TYPE=='author':
                    result_dict={'main':QUERY,'info':author_name}
                    print(author_name)
                if Q_TYPE=='time':
                    result_dict={'main':QUERY,'info':item_search_dict['publish_time'].encode('utf-8')}
                    print(item_search_dict['publish_time'].encode('utf-8'))
                if Q_TYPE=='prize':
                    result_dict={'main':QUERY,'info':item_search_dict['prize']}
                    print(item_search_dict['prize'])
                if Q_TYPE=='content':
                    result_dict={'main':QUERY,'info':item_search_dict['content']}
                    print(item_search_dict['content'])
                if Q_TYPE=='publisher':
                    result_dict={'main':QUERY,'info':publisher}
                    print(publisher)
                if Q_TYPE=='rating':
                    result_dict={'main':QUERY,'info':rating_score.encode('utf-8')}
                    print(rating_score.encode('utf-8'))
            return True,result_dict
        if ID_NAME=='AUTHOR' and item_search is not None:
            item_search_dict=dict(item_search)
            book=douban_graph.match_one(set([item_search]), r_type="book_author_is").   start_node
            book_name=book['name']
            publish_time=book['publish_time'].encode('utf-8')
            content=book['content']
            rating_score=douban_graph.match_one((book,),r_type="book_rating_is").end_node['score']
            category=douban_graph.match_one((book,),r_type="book_category_is").end_node['name'].replace('.xlsx','')
            publisher=douban_graph.match_one((book,),r_type="book_publisher_is").end_node['name']
            if Q_TYPE is None:
                result_dict={'main':QUERY,\
                    'info':book_name+' '+item_search_dict['name']+' '+category+' '  +rating_score.encode('utf-8')+' '+publisher+' '+publish_time+'\n' +content
                    }
                result_str=book_name+' '+item_search_dict['name']+' '+category+' '+rating_score.encode('utf-8')+' '+publisher+' '+publish_time+'\n'+content
                print(result_str)
            else:
                if Q_TYPE=='book':
                    item_search=matcher.match(ID_NAME,name=NAME).all()
                    book_list=[douban_graph.match_one(set([node]), r_type="book_author_is").start_node['name'].strip() for node in item_search]
                    book_str='\n'.join(list(set(book_list)))
                    print(book_str)
                    result_dict={'main':QUERY,'info':book_str}
            return True,result_dict
        else:
            return False,{'main':'您提出的问题暂时无法回答','info':''}
    except Exception:
        return False,{'main':'您提出的问题暂时无法回答','info':''}

def douban(request):
    ctx={'main':'','info':''}
    if request.POST:
        response={'main':'','info':''}
        query_str= request.POST['q']
        print(query_str)
        parse_items=rules(query_str)
        parse_entities=getNameEntity(query_str.encode('utf-8'))
        if parse_items is not None:
            _,response =searchKnowGraph(parse_items[0],parse_items[1],QUERY=query_str)
        elif parse_entities is not None:
            #response=[]
            if parse_entities[0]!='book':
                flag,res=searchKnowGraph('BOOK',parse_entities[1],parse_entities[0],query_str)
            else:
                flag,res=searchKnowGraph('AUTHOR',parse_entities[1],parse_entities[0],query_str)
            if flag is True:
                response=res
        else:
            response ={'main':'您提出的问题暂时无法回答','info':''}
        ctx=response
    return render(request, "search.html", {'ctx': ctx})
