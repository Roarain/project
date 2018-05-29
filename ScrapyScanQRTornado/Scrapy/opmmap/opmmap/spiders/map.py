# -*- coding: utf-8 -*-
import scrapy
import sys
from ..items import OpmmapItem
import re
import time
from scrapy.http import FormRequest, Request
from hall_infos import hall_infos
import logging
import copy
from scrapy.utils.request import request_fingerprint
from ..wredis import RedisPool
import hmac
import hashlib
import ujson

logging.basicConfig(filename='map.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

reload(sys)
sys.setdefaultencoding('utf-8')


class MapSpider(scrapy.Spider):

    name = 'map'
    allowed_domains = ['114.242.119.194']

    def __init__(self, *args, **kwargs):
        super(MapSpider, self).__init__(*args, **kwargs)
        self.url_start = 'http://114.242.119.194:9714/test.html'
        self.url_data = 'http://114.242.119.194:9714/infoplatform/hall/loadPrePareProData.action'

        self.counter = {}
        self.giveup = []
        self.hall_infos = copy.deepcopy(hall_infos)
        self.temp_hall_infos = copy.deepcopy(hall_infos)
        self.parameter_id = ('proId', 'areaId', 'hallId')
        self.form_data_login = {
            'referer': 'index.php',
            'login': 'jinf',
            'cookietime': '2592000',
            'password': 'jinf',
            'submit': '马上登陆',
        }

	self.salt = 'crrT4DOKDYPuqVJWl8cBFJMnr9KL0fB2ay1y2mDuQPOv8YIVHJaaGRso4CGCgKumw'

    def start_requests(self):
        return [Request(url=self.url_start, callback=self.post_login)]

    def post_login(self, response):
        return [FormRequest.from_response(
            response,
            headers=response.request.headers,
            formdata=self.form_data_login,
            callback=self.post_search_data,
        )]

    def post_search_data(self, response):
        for hall_info in self.hall_infos:
            post_data = dict(zip(self.parameter_id, hall_info))
            yield FormRequest(
                url=self.url_data,
                formdata=post_data,
                callback=self.parse,
                meta=post_data,
                dont_filter=True,
            )

    def parse(self, response):
        node_list = response.xpath("//tr[@bgcolor='#FFFFFF']")
        post_data = {k: v for k, v in response.meta.items() if k in self.parameter_id}
        post_data_hallId = post_data['hallId']

        if not node_list:
            logging.info('parse error post data: {}'.format(post_data))
            if post_data_hallId not in self.counter.keys():
                self.counter[post_data_hallId] = 1
            if self.counter[post_data_hallId] >= 20:
                logging.info('give up get data: {}'.format(post_data_hallId))
                return
            elif 0 < self.counter[post_data_hallId] < 20:
                self.counter[post_data_hallId] += 1
                logging.info('{} repeat times: {}'.format(post_data_hallId, self.counter[post_data_hallId]))
                time.sleep(5)
                yield FormRequest(
                    url=self.url_data,
                    formdata=post_data,
                    callback=self.parse,
                    meta=post_data,
                    dont_filter=True,
                )
        else:
            logging.info('parse post data: {}'.format(post_data))
            for node in node_list:
                item = OpmmapItem()
                proId = post_data['proId']
                areaId = post_data['areaId']
                hallId = post_data['hallId']
		
		proName = node.xpath("//select[@id='proId']/option[@selected='selected']/text()").extract()
                if proName:
                    proName = proName[0].encode('utf-8')
                else:
                    proName = ''
                areaName = node.xpath("//select[@id='areaId']/option[@selected='selected']/text()").extract()
                if areaName:
                    areaName = areaName[0].encode('utf-8')
                else:
                    areaName = ''
                hallName = node.xpath("//select[@id='hallId']/option[@selected='selected']/text()").extract()
                if hallName:
                    hallName = hallName[0].encode('utf-8')
                else:
                    hallName = ''

                terminal_id = node.xpath("./td[2]/strong/text()").extract()[0].encode('utf-8').replace('\t', '').replace(' ', '').replace('\r\n', '')
		key = proId + areaId + hallId + terminal_id
		key_hash = hmac.new(key, self.salt, hashlib.sha256).hexdigest() + 'A'
		
		d = dict(
			proId=proId,
			areaId=areaId,
			hallId=hallId,
			terminal_id=terminal_id,
			proName=proName,
			areaName=areaName,
			hallName=hallName,
		)

		js = ujson.dumps(d)
		
		item['key'] = key_hash
		item['value'] = js

                logging.info('get item data: {}'.format(item))
                yield item
