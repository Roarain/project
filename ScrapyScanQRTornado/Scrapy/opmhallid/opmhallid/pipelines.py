# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from wredis import RedisPool

import logging

class OpmhallidPipeline(object):
    def __init__(self):
	self.rp = RedisPool().redis_pool

    def process_item(self, item, spider):
	list_name = item['list_name']
	hall_info = item['hall_info']
	self.rp.lpush(list_name, hall_info)
	logging.info('pipeline lpush data: {}'.format(item))
        return item

    def close_spider(self, spider):
	pass
        #self.client.close()
