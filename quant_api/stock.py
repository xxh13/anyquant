#-*- coding:utf-8 -*-

"""
股票资源数据
"""

from settings import EXCHANGE, MIN_YEAR, MAX_YEAR, ERROR_CODE, START_TIME, END_TIME, FIELDS
from util import get_stock_code, get_stock_data
import falcon
import json
import re
import datetime


class StockAllResource:
	"""
	股票列表资源
	"""
	def __init__(self):
		pass

	def on_get(self, req, resp):
		year = req.get_param(name='year')
		exchange = req.get_param(name='exchange')

		# 参数异常没有的处理,按照默认参数填充
		if year == None or exchange == None:
			resp.status = falcon.HTTP_200
			to_return_info = {'status': 'ok', 'data':[]}
			if year == None:
				year = datetime.datetime.now() - datetime.timedelta(days=365)      # 默认开始时间
			else:
				year = datetime.datetime.strptime(str(year),'%Y')
			if exchange == None:
				exchange = EXCHANGE
			else:
				exchange = [exchange]
			stock_code = get_stock_code(year, exchange)
			for code in stock_code:
				to_return_info['data'].append({'name': code[0], 'link': '~/api/stock/' + code[0]})
			resp.body=json.dumps(to_return_info)
		else:
			try:
				year = int(year)
			except:
				resp.status = falcon.HTTP_400
				error_description = 'wrong param value with param year, param year should be a integer'
				resp.body=json.dumps({'status': 'error', 'data': error_description,
										'error_code': ERROR_CODE['INVALID_PARAM_VALUE']})

			if not (year > MIN_YEAR and year < MAX_YEAR) :
				resp.status = falcon.HTTP_400
				error_description = 'wrong param value, param year should in range of (2006, now)'
				resp.body=json.dumps({'status': 'error', 'data': error_description,
										'error_code': ERROR_CODE['INVALID_PARAM_VALUE']})
			elif exchange not in EXCHANGE:
				resp.status = falcon.HTTP_400
				error_description = 'wrong param exhange, param exchange should in [sh, sz]'
				resp.body=json.dumps({'status': 'error', 'data': error_description,
										'error_code': ERROR_CODE['INVALID_PARAM_VALUE']})
			else:
				# 正常情况处理
				to_return_info = {'status': 'ok', 'data':[]}
				resp.status = falcon.HTTP_200
				stock_code = get_stock_code(datetime.datetime.strptime(str(year),'%Y'), [exchange])
				for code in stock_code:
					to_return_info['data'].append({'name': code[0], 'link': '~/api/stock/'+code[0]})
				resp.body=json.dumps(to_return_info)


class StockResource:
	"""
	股票单个信息,默认返回过去一个月全部交易数据
	"""
	def __init__(self):
		pass

	def on_get(self, req, resp, stock_code):
		start = req.get_param('start')
		end = req.get_param('end')
		fields = req.get_param('fields')
		if start == None:
			start  = START_TIME
		else:
			if re.match(r'^\d\d\d\d-\d\d-\d\d$',start) == None:
				error_description = 'invalid param value with start, the format of start should be YYYY-MM-DD'
				resp.status = falcon.HTTP_400
				resp.body = json.dumps({'status': 'error', 'data': error_description,
											'error_code': ERROR_CODE['INVALID_PARAM_VALUE']})
				return

		if end == None:
			end = END_TIME
		else:
			if re.match(r'^\d\d\d\d-\d\d-\d\d$',end) == None:
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
				error_description = 'invalid param value with fields,valid fields refer to ~/api/stock/fields'
				resp.status = falcon.HTTP_400
				resp.body = json.dumps({'status': 'error', 'data': error_description,
											'error_code': ERROR_CODE['INVALID_PARAM_VALUE']})
				return

		# 参数正常的情况处理
		to_return_info = {'status': 'ok', 'data':{'name': stock_code} }
		resp.status = falcon.HTTP_200
		to_return_info['data']['trading_info'] = get_stock_data(stock_code, start, end, fields)
		resp.body = json.dumps(to_return_info)


class StockUtilResurce:
	"""
	数据所有可用字段
	"""
	def __init__(self):
		pass

	def on_get(self, req, resp):
		to_return_info = {'status': 'ok', 'data':FIELDS}
		resp.status = falcon.HTTP_200
		resp.body = json.dumps(to_return_info)