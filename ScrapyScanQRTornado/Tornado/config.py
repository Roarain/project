# -*- coding: utf-8 -*-

import logging

logging.basicConfig(filename='conf.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

server_port = 9999

redis_options = {
	'redis_host': '192.168.122.66',
	'redis_port': 6379,
	'redis_password': '',
	'redis_db': 0,
	'redis_timeout': 3600,
}
