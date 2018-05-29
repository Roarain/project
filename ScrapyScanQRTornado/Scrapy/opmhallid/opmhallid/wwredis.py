# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 2018/5/22 15:47
@contact: welovewxy@126.com
@file: wwredis.py
@license: Apache Licence
@site: 
@software: PyCharm
"""
import redis
import logging

logging.basicConfig(filename='wwredis.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)


class RedisPool(object):
    def __init__(self):
        if not hasattr(RedisPool, 'redis_pool'):
            RedisPool.redis_pool = self.create_redis_pool()
        if not hasattr(RedisPool, 'redis_timeout'):
            RedisPool.redis_timeout = 3600

    @staticmethod
    def create_redis_pool():
        pool = redis.ConnectionPool(host='127.0.0.1',
                                    port=3379,
                                    db=0)
        RedisPool.redis_pool = redis.Redis(connection_pool=pool)
        return RedisPool.redis_pool

    def setex(self, key, value):
        """
        from dict to redis string with timeout
        :param key:
        :param value:
        :return: None
        """
        try:
            self.redis_pool.setex(key, value, self.redis_timeout)
            logging.info('Execute SETEX Success, key: {0}, value: {1}'.format(key, value))
        except Exception as e:
            logging.debug('Execute SETEX Faild, key: {0}, value: {1}'.format(key, value))

    def get(self, key):
        """
        according to key to get string type's value
        :param key:
        :return:value
        """
        try:
            result = self.redis_pool.get(key).decode()
            result = eval(result)
            self.redis_pool.expire(key, self.redis_timeout)
            logging.info('Execute GET Success, key: {0}'.format(key))
            return result
        except Exception as e:
            logging.debug('Execute GET Faild, key: {0}'.format(key))
            result = None
        return result

    def hmset(self, key, mapping):
        """
        hash type
        :param key:
        :param mapping:dict
        :return: None
        """
        try:
            self.redis_pool.hmset(key, mapping)
            self.redis_pool.expire(key, self.redis_timeout)
            logging.info('Execute HMSET Success, key: {0}, mapping: {1}'.format(key, mapping))
        except Exception as e:
            logging.debug('Execute HMSET Faild, key: {0}, mapping: {1}'.format(key, mapping))

    def hgetall(self, key):
        """
        according to key to get hash type's value
        :param key:
        :return: mapping(dict)
        """
        try:
            bresult = self.redis_pool.hgetall(key)
            result = {key.decode(): value.decode() for (key, value) in bresult.items()}
            self.redis_pool.expire(key, self.redis_timeout)
            logging.info('Execute HGETALL Success, key: {0}'.format(key))
        except Exception as e:
            logging.debug('Execute HGETALL Faild, key: {0}'.format(key))
            result = None
        return result

    def exists(self, key):
        """

        :param key:
        :return:True/False
        4556
        """
        return self.redis_pool.exists(key)

    def hget(self, key, field):
        """
        hash hget key, field
        :param key:
        :param field:
        :return: key-->field-->value
        """
        try:
            result = self.redis_pool.hget(key, field).decode()
            result = eval(result)
        except Exception as e:
            logging.debug('Execute HGET Faild, key: {0}, field: {1}'.format(key, field))
            result = self.redis_pool.hget(key, field)
        return result

