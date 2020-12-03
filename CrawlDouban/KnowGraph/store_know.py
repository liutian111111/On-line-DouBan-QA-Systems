#coding=utf-8
from py2neo import Node, Relationship, Graph, NodeMatcher
import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

douban_graph= Graph(
    "http://localhost:7474", 
    username="neo4j", 
    password="neo4j"
)
douban_graph.delete_all()

json_file='./data/douban_info.json'

def writeKnowGraph():
    with codecs.open(json_file,'r+','utf-8') as fin:
        lines=fin.readlines()
        for line in lines:
            book_dict=json.loads(line)
            if book_dict['name'] is not None:
                book_name=book_dict['name'].strip()
            if book_dict['pubtime'] is not None:
                book_pubtime=str(book_dict['pubtime']).strip()
            if book_dict['prize'] is not None:
                book_prize=str(book_dict['prize']).strip()
            if book_dict['content'] is not None:
                book_content=book_dict['content'].strip()
            if book_dict['author'] is not None:
                book_author=book_dict['author'].strip()
            if book_dict['rating'] is not None:
                book_rating=str(book_dict['rating']).strip()
            if book_dict['review_num'] is not None:
                book_review_num=str(book_dict['review_num']).strip()
            if book_dict['category'] is not None:
                book_category=book_dict['category'].strip().replace('.xlsx','')
            if book_dict['publisher'] is not None:
                book_publisher=book_dict['publisher'].strip()
            book_entity=Node('BOOK',name=book_name)
            book_entity['publish_time']=book_pubtime
            book_entity['prize']=book_prize
            book_entity['content']=book_content
            author_entity=Node('AUTHOR',name=book_author)
            rating_entity=Node('RATING',score=book_rating)
            rating_entity['review_num']=book_review_num
            category_entity=Node('CATEGORY',name=book_category)
            publish_entity=Node('PUBLISHER',name=book_publisher)
            #douban_graph.create(book_entity)
            #douban_graph.create(author_entity)
            #douban_graph.create(rating_entity)
            #douban_graph.create(category_entity)
            #douban_graph.create(publish_entity)
            book_author_relation=Relationship.type('book_author_is',)
            BA=book_author_relation(book_entity,author_entity)
            book_rating_relation=Relationship.type('book_rating_is')
            BR=book_rating_relation(book_entity,rating_entity)
            book_category_relation=Relationship.type('book_category_is')
            BC=book_category_relation(book_entity,category_entity)
            book_publisher_relation=Relationship.type('book_publisher_is')
            BP=book_publisher_relation(book_entity,publish_entity)
            #print(book_author_relation.type())
            douban_graph.create(BA)
            douban_graph.create(BR)
            douban_graph.create(BC)
            douban_graph.create(BP)

def searchKnowGraph(ID_NAME=None,NAME=None):
    matcher=NodeMatcher(douban_graph)
    item_search=matcher.match(ID_NAME,name=NAME).first()
    item_search_dict=dict(item_search)
    print(type(item_search_dict))
    for k in item_search_dict:
        print(k)
        print(item_search_dict[k].strip())

if __name__=='__main__':
    #searchKnowGraph('BOOK','Stories of Your Life and Others')
    writeKnowGraph()
