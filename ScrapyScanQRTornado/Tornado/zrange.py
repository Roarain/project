#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
import redis

pool = redis.ConnectionPool(host='127.0.0.1',port=6379,db=0,)
redis_pool = redis.Redis(connection_pool=pool)

result = redis_pool.zrange('834b36d0d85b33562208c9813399d2b75db71ead9f4f4d923737ca2ac9c6c6f8', -10, -1, withscores=True)
print result
