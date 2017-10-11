#-*- coding:utf-8 -*-

"""
benchmark 资源数据
"""

import falcon
from settings import HOST, PORT, MIN_YEAR, MAX_YEAR, ERROR_CODE, START_BENCH_TIME, END_TIME, FIELDS, BENCHMARK_NAME
from util import get_benchmark_data
import json
import re
import datetime

class BenchmarkAllResource:
	"""
	benmark 列表信息
	"""
	def __init__(self):
		#TODO
		pass

	def on_get(self, req, resp):
		to_return_info = {'status': 'ok', 'data':[]}
		resp.status = falcon.HTTP_200
		to_return_info['data'].append({'name': 'hs300', 'link': 'http://'+HOST+':'+PORT+'/api/benchmark/hs300'})
		resp.body=json.dumps(to_return_info)

class BenchmarkResource:
	"""
	benchmark 单个信息
	"""
	def __init__(self):
		#TODO
		pass

	def on_get(self, req, resp, benchmark_name):
		#TODO
		start = req.get_param('start')
		end = req.get_param('end')
		fields = req.get_param('fields')
		if start == None:
			start  = START_BENCH_TIME
		else:
			if re.match(r'^\d{4}-\d\d-\d\d$', start) == None:
				error_description = 'invalid param value with start, the format of start should be YYYY-MM-DD'
				resp.status = falcon.HTTP_400
				resp.body = json.dumps({'status': 'error', 'data': error_description,
											'error_code': ERROR_CODE['INVALID_PARAM_VALUE']})
				return

		if end == None:
			end = END_TIME
		else:
			if re.match(r'^\d{4}-\d\d-\d\d$',end) == None:
				error_description = 'invalid param value with end, the format of end should be YYYY-MM-DD'
				resp.status = falcon.HTTP_400
				resp.body = json.dumps({'status': 'error', 'data': error_description,
											'error_code': ERROR_CODE['INVALID_PARAM_VALUE']})
				return

		if fields == None:
			fields = FIELDS
		else:
			fields = fields.split(' ')
			if not set(fields).issubset(set(FIELDS)):
				error_description = 'invalid param value with fields,valid fields refer to ~/api/benchmark/fields'
				resp.status = falcon.HTTP_400
				resp.body = json.dumps({'status': 'error', 'data': error_description,
											'error_code': ERROR_CODE['INVALID_PARAM_VALUE']})
				return
		benchmark_code = BENCHMARK_NAME[benchmark_name]
		# 参数正常的情况处理
		to_return_info = {'status': 'ok', 'data':{'name': benchmark_name} }
		resp.status = falcon.HTTP_200
		to_return_info['data']['trading_info'] = get_benchmark_data(benchmark_code, start, end, fields)
		resp.body = json.dumps(to_return_info)