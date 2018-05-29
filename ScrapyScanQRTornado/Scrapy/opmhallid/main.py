# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 2018/5/21 17:04
@contact: welovewxy@126.com
@file: main.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import logging
from scrapy import cmdline

logging.basicConfig(filename='main.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)

cmdline.execute("scrapy crawl hallid".split())