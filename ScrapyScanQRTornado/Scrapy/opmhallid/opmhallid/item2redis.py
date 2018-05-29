# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 2018/5/22 14:44
@contact: welovewxy@126.com
@file: item2redis.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import logging
from wwredis import RedisPool
from functools import reduce
import hashlib
import hmac
import ujson
import time
import redis

logging.basicConfig(filename='item2redis.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)
'''
salt = 'crrT4DOKDYPuqVJWl8cBFJMnr9KL0fB2ay1y2mDuQPOv8YIVHJaaGRso4CGCgKumw'
d1 = {"areaId":"417","hallId":"417006","proName":"辽宁","proId":"6","hallName":"辽宁省营口市龙源花园","areaName":"营口市"}

d1_key = reduce(lambda x, y: x + y, list([d1['proId'], d1['areaId'], d1['hallId']]))
print d1_key
# d1_key_hash = hmac.new(bytes(str(d1_key), 'utf-8'), bytes(salt, 'utf-8'), hashlib.sha256).hexdigest()
d1_key_hash = hmac.new(d1_key, salt, hashlib.sha256).hexdigest()
print d1_key_hash
d1_json = ujson.dumps(d1)
print d1_json
print type(d1_json)

RedisPool().hmset(d1_key_hash, d1_json)

'''

date = time.strftime("%Y%m%d")
incr = date + "0001"
incr_name = "incr_" + incr
print 'ori incr: ', incr
print incr_name
pool = redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
redis_pool = redis.Redis(connection_pool=pool)
redis_pool.set(incr_name, incr)

print 'incr 1: ', redis_pool.get(incr_name)
redis_pool.incr(incr_name)
print 'incr 2: ', redis_pool.get(incr_name)

redis_pool.zrange()

# zrange(self, name, start, end, desc=False, withscores=False,score_cast_func=float)
redis_pool.zrange(
    name='a',
    start=-4,
    end=-1,
    score_cast_func=int,
)




