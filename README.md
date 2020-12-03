# On-line-DouBan-QA-Systems

豆瓣知识问答环境部署和配置文档

一、	软件运行需求：
Python2+、java8.0+、neo4j-community-3.5.23、Scrapy爬虫框架、Django、命名实体识别工具LAC

二、	安装过程：
1.	安装python 2版本以及java 8.0以上工具：
2.	安装neo4j-community-3.5.23:
https://neo4j.com/docs/operations-manual/3.5/installation/
3.	安装Python相关软件包：
（1）	py2neo包
pip install py2neo
参考文档：https://py2neo.org/v3/
（2）	scrapy包（推荐版本1.8.0）
pip install scrapy 或 pip install scrapy==1.8.0
参考文档：https://docs.scrapy.org/en/latest/intro/install.html
（3）	django包（推荐版本1.11.21）
pip install Django 或 pip install Django== 1.11.21
（4）	LAC包
pip install LAC

三、	运行步骤
1.	运行neo4j
参考文档：https://neo4j.com/download-center/-community
2.	解压缩文件CrawlDouban.zip
3.	进入目录 ./CrawlDouban/KnowGraph，存储数据到neo4j
python store_know.py
4.	存储好数据之后，进入./CrawlDouban/KnowGraph/DouBan/目录
python manage.py runserver 0.0.0.0:6006
5.	进入浏览器，查看运行网页：
http://0.0.0.0:56006/search

四、	文件描述：
1.	./CrawlDouban/CrawlDouban：爬虫的主要代码（Scrapy架构）
2.	./CrawlDouban/KnowGraph：Django网页服务器的相关代码、neo4j相关代码、命名实体识别及正则匹配相关代码
（1）	./store_know.py 知识图谱的定义及存储程序
（2）	./CrawlDouban/KnowGraph/DouBan/DouBan/views.py
函数searchKnowGraph()：neo4j知识图谱查询代码
函数rules()：常规问题查询程序
函数rulesForEntity()：命名实体识别程序（基于规则-正则表达式）
函数getNameEntity()：命名实体识别程序（基于模型识别）
（3）	./CrawlDouban/KnowGraph/DouBan/template/search.html：网页源代码

