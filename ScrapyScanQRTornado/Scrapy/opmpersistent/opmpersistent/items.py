# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OpmpersistentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
    # 终端机实时数据监控
    # telminal
    terminal_id = scrapy.Field()                            # 终端机ID
    terminal_status = scrapy.Field()                        # 终端机状态
    terminal_login_nums = scrapy.Field()                    # 终端机登陆人数
    terminal_last_login_time = scrapy.Field()               # 终端机最后登陆时间
    terminal_last_checkout_time = scrapy.Field()            # 终端机最后签退时间
    terminal_sale = scrapy.Field()                          # 终端机销售额
    '''
    '''
    # 销售厅实时数据监控
    # hall
    proId = scrapy.Field()                                  # 省ID
    areaId = scrapy.Field()                                 # 市ID
    hallId = scrapy.Field()                                 # 大厅ID
    proName = scrapy.Field()                                # 省名称
    areaName = scrapy.Field()                               # 市名称
    hallName = scrapy.Field()                               # 大厅名称

    terminal_id = scrapy.Field()                            # 终端机ID
    terminal_sale = scrapy.Field()                          # 终端机销售额
    terminal_sale_percent = scrapy.Field()                  # 终端机销售占总销售比
    terminal_winning = scrapy.Field()                       # 终端机中奖金额
    terminal_redemption_percent = scrapy.Field()            # 终端机返奖率
    terminal_single_bet = scrapy.Field()                    # 终端机平均单次投注额
    '''
    key = scrapy.Field()                                    # redis zadd key data score for persistent data week,month,year
    data = scrapy.Field()
    score = scrapy.Field()
