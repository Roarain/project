#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import redis
import logging

logging.basicConfig(filename='wredis.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class RedisPool(object):
    def __init__(self):
        if not hasattr(RedisPool, 'redis_pool'):
            RedisPool.redis_pool = self.create_redis_pool()
    
    @staticmethod
    def create_redis_pool():
        pool = redis.ConnectionPool(host='192.168.122.66',
                                    port=6378,
                                    db=0)
        RedisPool.redis_pool = redis.Redis(connection_pool=pool)
        return RedisPool.redis_pool


'''
if __name__ == '__main__':
    rp = RedisPool().redis_pool
    rp.set('a', 5)
    result = rp.get('a')
    print result
    rp.incr('a')
    result = rp.get('a')
    print result
'''
