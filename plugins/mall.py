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

class MallPlugin(Plugin):
    
    def __init__(self):
        self.urls = data.mall_urls

    #self.url = "https://www.smzdm.com/mall/cebbank/"
    def start(self):
        for url in self.urls:
            content = crawler.fetch_content(url)
            tree = html.fromstring(content)
            matches = tree.xpath('//ul/li/div[@class="listItem"]/h2[@class="itemName"]/a')
            #print matches
            
            news_dict = {}
            for m in matches:
                title = self.format_str(m.xpath('span[@class="black"]/text()')[0])
                highlight= self.format_str(m.xpath('span[@class="red"]/text()')[0])
                #print "%s: %s" % (title, highlight)
                hash = md5.new("%s%s"%(title,highlight)).hexdigest() 
                content = self.format_str(m.attrib.get("href"))
                content = "%s %s" % (content, hash)
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
    
    
    
    
