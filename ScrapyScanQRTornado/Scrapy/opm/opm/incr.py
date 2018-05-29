# -*- coding: utf-8 -*-

import redis
import time
from wredis import RedisPool

yyyymmdd = time.strftime("%Y%m%d")
incr_name = 'incr_' + yyyymmdd
rp = RedisPool().redis_pool
if not rp.exists(incr_name):
        incr = yyyymmdd + "0001"
        rp.set(incr_name, incr)
else:
	rp.incr(incr_name)
incr = rp.get(incr_name)
