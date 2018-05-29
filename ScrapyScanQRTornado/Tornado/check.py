# -*- coding: utf-8 -*-


import functools
import logging

def check_parameter(function):
	@functools.wraps(function)
	def _wrapper(self, *args, **kwargs):
		temp_id = self.get_argument('temp_id', '')
		if not temp_id:
			logging.info('temp_id not given, reject request...')
			self.render('error.html')
			return
		temp_num = int(temp_id[10:16])
		if not 300000 < temp_num < 900000:
			logging.info('temp_id invalid, reject request...')
			self.render('error.html')
			return
		terminal_id = self.get_argument('terminal_id', '')
		if not terminal_id:
			logging.info('terminal_id not given, reject request...')
			self.render('error.html')
			return
		logging.info('authentication passed, terminal_id: {}, temp_id: {}'.format(terminal_id, temp_id))
		return function(self, *args, **kwargs)
	return _wrapper
