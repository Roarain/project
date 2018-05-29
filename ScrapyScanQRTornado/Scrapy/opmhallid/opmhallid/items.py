# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OpmhallidItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
    proId = scrapy.Field()                                  # 省ID
    areaId = scrapy.Field()                                 # 市ID
    hallId = scrapy.Field()                                 # 大厅ID
    proName = scrapy.Field()                                # 省名称
    areaName = scrapy.Field()                               # 市名称
    hallName = scrapy.Field()                               # 大厅名称
    '''
    list_name = scrapy.Field()		#redis rpush name *value	
    hall_info = scrapy.Field()
