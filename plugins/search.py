#!/usr/bin/env python

from lxml import html
import md5 
from parser.entity import * 
import redis
import config 
from crawler import crawler
from utils import notification
from plugins import Plugin
import data

class SearchPlugin(Plugin):

    def __init__(self):
        self.urls = data.search_urls

    #self.url = "http://search.smzdm.com/?c=home&s=%E5%85%89%E5%A4%A7&order=score&mall_id=1065"
    def start(self):
        for url in self.urls:
            content = crawler.fetch_content(url)
            tree = html.fromstring(content)
            #matches = tree.xpath('//div[@class="z-feed-content"]/h5/a')
            matches = tree.xpath('//ul[@id="feed-main-list"]/li/div/div[@class="z-feed-content"]')
            #print matches
            
            news_dict = {}
            for m in matches:
                title = self.format_str(m.xpath('h5[@class="feed-block-title"]/a/text()')[0])
                link = self.format_str(m.xpath('h5[@class="feed-block-title"]/a')[0].attrib.get("href"))
                #print title
                highlight = self.format_str(m.xpath('h5[@class="feed-block-title"]/a/div[@class="z-highlight"]/text()')[0])
                #print highlight
                content = self.format_str(m.xpath('div[@class="feed-block-descripe"]/text()')[0])
                hash = md5.new("%s%s"%(title,highlight)).hexdigest() 
                content = "%s %s %s" % (content, link, hash)
                entity = NewsEntity(title, highlight, content)
                #print hash
                news_dict[hash] = entity

            r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
            
            for hash, entity in news_dict.iteritems():
                if r.get(hash) == None:
                    self.notify_user(entity)
                    r.set(hash, entity)
        
    
    
    def format_str(self, str):
        return str.encode('utf8').strip()
    
    def notify_user(self, entity):
        print "Adding new entity %s..." % entity.title
        notification.sendmail(entity.title,  "%s\n%s"%(entity.highlight, entity.content))
    
    
    
    
