#-*- coding:utf-8 -*-

"""
setttings for the api 
"""
import datetime

# 交易所范围
EXCHANGE = ['sh', 'sz']

# 股票列表查找年份范围,从2006年至今,默认是以今天截至前一年的范围
MIN_YEAR = 2006
MAX_YEAR = datetime.datetime.now().year

# 个股查找默认时间范围，默认返回前面30天的数据
START_TIME = datetime.datetime.now() - datetime.timedelta(days=30)
END_TIME = datetime.datetime.now()

# 股票基本属性
FIELDS_BASE = ['open', 'high', 'low', 'close', 'adj_price', 'volume']
# 股票高阶数据
FIELDS_SENIOR = ['turnover', 'pe_ttm', 'pb']
# 所有数据
FIELDS = FIELDS_BASE + FIELDS_SENIOR

#  错误码定义
ERROR_CODE = {
    'INVALID_PARAM': '001',
    'INVALID_PARAM_VALUE': '002'
}

# 数据库的参数
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quant_base',
        'HOST':  '121.41.106.89',
        'PORT': '3306',
        'USER': 'quant',
        'PASSWORD':  'Sydar10',
    }
}

HOST = 'localhost'
PORT = '8000'

BENCHMARK_NAME = {'hs300': 'sh000300'}

START_BENCH_TIME = datetime.datetime.now() - datetime.timedelta(days=365)