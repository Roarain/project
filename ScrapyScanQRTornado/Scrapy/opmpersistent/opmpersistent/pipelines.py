# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from wredis import RedisPool
import logging

class OpmpersistentPipeline(object):
    def __init__(self):
	self.rp = RedisPool().redis_pool

    def process_item(self, item, spider):
	key = item['key']
	data = item['data']
	score = item['score']
	self.rp.zadd(key, data, score)
	logging.info('pipeline zadd data: {}'.format(item))
        return item

    def close_spider(self, spider):
	pass
        #self.client.close()
