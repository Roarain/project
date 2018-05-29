#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import redis
import logging
import rediscluster
from rediscluster import StrictRedisCluster, StrictClusterPipeline


logging.basicConfig(filename='wredis.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class RedisCluster(object):
    def __init__(self):
        if not hasattr(RedisCluster, 'redis_cluster'):
            RedisCluster.redis_cluster = self.create_redis_cluster()
        if not hasattr(RedisCluster, 'redis_cluster_pipeline'):
            RedisCluster.redis_cluster_pipeline = self.create_redis_cluster_pipeline()
    
    @staticmethod
    def create_redis_cluster():
	startup_nodes = [
		{"host": "192.168.122.66", "port": "6379"},
		{"host": "192.168.122.66", "port": "6380"},
		{"host": "192.168.122.66", "port": "6381"},
		{"host": "192.168.122.66", "port": "6382"},
		{"host": "192.168.122.66", "port": "6383"},
		{"host": "192.168.122.66", "port": "6384"},
	]
	RedisCluster.redis_cluster = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        return RedisCluster.redis_cluster

    @staticmethod
    def create_redis_cluster_pipeline():
        startup_nodes = [
                {"host": "192.168.122.66", "port": "6379"},
                {"host": "192.168.122.66", "port": "6380"},
                {"host": "192.168.122.66", "port": "6381"},
                {"host": "192.168.122.66", "port": "6382"},
                {"host": "192.168.122.66", "port": "6383"},
                {"host": "192.168.122.66", "port": "6384"},
        ]
        RedisCluster.redis_cluster = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        RedisCluster.redis_cluster_pipeline = RedisCluster.redis_cluster.pipeline()
        return RedisCluster.redis_cluster_pipeline
#'''
if __name__ == '__main__':
    rc = RedisCluster().redis_cluster
    rcp = RedisCluster().redis_cluster_pipeline
    #rp = RedisPool().redis_pool
    rc.set('a', 5)
    result = rc.get('a')
    print result
    rc.incr('a')
    result = rc.get('a')
    print result
    print rcp.set('b',2).incr('b').incr('b').pipeline()
#'''
