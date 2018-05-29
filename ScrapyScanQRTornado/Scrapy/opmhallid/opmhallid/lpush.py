#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
import ujson
import hmac,hashlib
from functools import reduce
import time

pool = redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
redis_pool = redis.Redis(connection_pool=pool)


lrange = redis_pool.lrange('mylist', 0, -1)
print 'lrange: ', lrange
print 'type lrange: ', type(lrange)


