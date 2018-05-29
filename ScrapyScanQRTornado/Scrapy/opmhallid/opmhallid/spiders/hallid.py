# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import time
from scrapy.http import FormRequest, Request
from ..items import OpmhallidItem
import logging
import ujson


reload(sys)
sys.setdefaultencoding('utf-8')


class HallidSpider(scrapy.Spider):
    name = 'hallid'
    allowed_domains = ['114.242.119.194']

    def __init__(self, *args, **kwargs):
        super(HallidSpider, self).__init__(*args, **kwargs)
        self.counter = {}
        self.temp_hall = []
        self.parameter_id = ('proId', 'areaId', 'hallId')
        self.parameter_name = ('proName', 'areaName', 'hallName')
        self.url_start = 'http://114.242.119.194:9714/test.html'
        self.url_data = 'http://114.242.119.194:9714/infoplatform/hall/loadPrePareProData.action'
        self.form_data_login = {
            'referer': 'index.php',
            'login': 'jinf',
            'cookietime': '2592000',
            'password': 'jinf',
            'submit': '马上登陆',
        }

        self.form_data_prepare_area_dict = {
            'proId': '6',
            'areaId': '00',
            'hallId': '00',
        }
        self.proId = '6'
        self.proName = '辽宁'

    def start_requests(self):
        return [Request(url=self.url_start, callback=self.post_login)]

    def post_login(self, response):
        return [FormRequest.from_response(
            response,
            headers=response.request.headers,
            formdata=self.form_data_login,
            callback=self.prepare_area_dict,
        )]

    def prepare_area_dict(self, response):
        yield FormRequest(
            url=self.url_data,
            headers=response.request.headers,
            formdata=self.form_data_prepare_area_dict,
            meta=self.form_data_prepare_area_dict,
            callback=self.search_area,
            dont_filter=True,
        )

    def search_area(self, response):
        area_infos_temp = response.xpath("//select[@id='areaId']/option[@value!='00']").extract()
        for area_info_temp in area_infos_temp:
            area_info_match_group = re.search('value="(.*)".*>(.*)<', area_info_temp.encode('utf-8'))
            area_name = area_info_match_group.group(2)
            area_id = area_info_match_group.group(1)
            hall_id = area_id + "001"
            form_data_hall_dict = dict(
                areaId=area_id,
                hallId=hall_id,
                proId=self.proId,
            )
            self.temp_hall.append(form_data_hall_dict)

        if self.temp_hall:
            for key, value in enumerate(self.temp_hall):
                logging.info('Loop HallId Request {} times, data: {}'.format(key, value))
                form_data_temp_hall = value
                yield FormRequest(
                    url=self.url_data,
                    headers=response.request.headers,
                    formdata=form_data_temp_hall,
                    meta=form_data_temp_hall,
                    callback=self.parse,
                    dont_filter=True,
                )

    def parse(self, response):
        area_name = response.xpath("//select[@id='areaId']/option[@selected='selected']/text()").extract()
        post_data = {k: v for k, v in response.meta.items() if k in self.parameter_id}
        post_data_areaId = post_data['areaId']
        if not area_name:
            logging.info('parse error post data: {}'.format(post_data))
            if post_data_areaId not in self.counter.keys():
                self.counter[post_data_areaId] = 1
            if self.counter[post_data_areaId] >= 10:
                logging.info('give up get data: {}'.format(post_data_areaId))
                return
            elif 0 < self.counter[post_data_areaId] < 10:
                self.counter[post_data_areaId] += 1
                logging.info('{} repeat times: {}'.format(post_data_areaId, self.counter[post_data_areaId]))
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
            area_name = area_name[0].encode('utf-8')
            hall_infos_temp = response.xpath("//select[@id='hallId']/option[@value!='00']").extract()
            for hall_info_temp in hall_infos_temp:
                item = OpmhallidItem()
                hall_info_match_group = re.search('value="(.*)".*>(.*)<', hall_info_temp.encode('utf-8'))
                hall_name = hall_info_match_group.group(2)
                hall_id = hall_info_match_group.group(1)
		t = tuple(
			(self.proId, post_data_areaId, hall_id)
		)
		js = ujson.dumps(t)
		'''
                item['proId'] = self.proId
                item['areaId'] = post_data_areaId
                item['hallId'] = hall_id
                item['proName'] = self.proName
                item['areaName'] = area_name
                item['hallName'] = hall_name
		'''
		
		item['list_name'] = 'hall_infos'
		item['hall_info'] = js
		
                logging.info('item data: {}'.format(item))
                yield item
