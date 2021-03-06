# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.options import define, options
import tornado.escape
from tornado.escape import xhtml_escape, xhtml_unescape
import time
from wredis import RedisPool
import ujson
import config
import datetime
import os
import sys
from check import check_parameter
import logging

logging.basicConfig(filename='terminalinfo.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
reload(sys)
sys.setdefaultencoding('utf-8')

define('port', default=9999, help='run on the given port', type=int)

translate_dict = {
	'terminal_single_bet': '终端机平均单次投注金额',
	'terminal_winning': '终端机中奖金额',
	'terminal_sale': '终端机销售金额',
	'terminal_sale_percent': '终端机销售占总销售比',
	'terminal_redemption_percent': '终端机返奖率',
        'proId': '省ID',
        'areaId': '市ID',
        'hallId': '大厅ID',
        'proName': '省名称',
        'areaName': '市名称',
        'hallName': '大厅名称',
        'terminal_id': '终端机ID',
}

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", Main),
			(r"/terminal", TerminalInfo),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), 'templates'),
			static_path=os.path.join(os.path.dirname(__file__), 'static'),
			xsrf_cookies=True,
			autoescape=None,
		)
		super(Application, self).__init__(handlers, **settings)

class Main(tornado.web.RequestHandler):
	def get(self):
		return self.write('Hello World!')

class TerminalInfo(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def get(self):
		yield self.main()
	
	@tornado.gen.coroutine
	def post(self):
		yield self.main()
	
	@check_parameter
	def main(self):
		self.set_header('server', 'GFW')
		terminal_id = self.get_argument('terminal_id', '')
		terminal_id_A = terminal_id + 'A'
		terminal_id_P = terminal_id + 'P'
	 
		redis_pipe = RedisPool().redis_pipe
		# physical_all_info, current, week, month
		redis_result = redis_pipe.get(terminal_id_A).zrange(terminal_id, -1, -1, withscores=True).zrange(terminal_id_P, -7, -1, withscores=True).zrange(terminal_id_P, -30, -1, withscores=True).execute()
		logging.info('redis_result: {}'.format(redis_result))

		physical_info_ori = ujson.loads(redis_result[0])
		physical_info = dict()
		for key, value in physical_info_ori.items():
			physical_info[translate_dict[key]] = value
		logging.info('physical_info: {}'.format(physical_info))

		redis_result_current = redis_result[1][0]
		current_info_ori = ujson.loads(redis_result_current[0])
		current_info = dict()
		for key, value in current_info_ori.items():
			current_info[translate_dict[key]] = value
		current_date = str(int(redis_result_current[1]))[:8]
		logging.info('current_date: {}, current_info: {}'.format(current_date, current_info))
		
		redis_result_weekly = redis_result[2]
		weekly_date = [str(int(i[1]))[:8] for i in redis_result_weekly]
		weekly_list = [ujson.loads(i[0]) for i in redis_result_weekly]
		#weekly_info = dict(date=weekly_date,)
		weekly_info = dict()
		for j in weekly_list[0].keys():
			result = []
			for i in weekly_list:
				result.append(str(i[j]).replace('%', ''))
			weekly_info[translate_dict[j]] = result
		logging.info('weekly_info: {}'.format(weekly_info))
		
		redis_result_monthly = redis_result[3]
		monthly_date = [str(int(i[1]))[:8] for i in redis_result_monthly]
		monthly_list = [ujson.loads(i[0]) for i in redis_result_monthly]
		#monthly_info = dict(date=monthly_date,)
		monthly_info = dict()
		for j in monthly_list[0].keys():
                        result = []
                        for i in monthly_list:
                                result.append(str(i[j]).replace('%', ''))
                        monthly_info[translate_dict[j]] = result
		logging.info('monthly_info: {}'.format(monthly_info))
		
		result_dict = dict(
				physical_info=physical_info,
				current_info=current_info,
				weekly_info=weekly_info,
				weekly_date=weekly_date,
				monthly_info=monthly_info,
				monthly_date=monthly_date,
			)
		logging.info('result_dict: {}'.format(result_dict))
		'''
		result_json = ujson.dumps(result_dict)
		#self.write(result_json)
		'''
		self.render('index.html', **result_dict)


def main():
	app = Application()
	app.listen(options.port)
	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	main()
