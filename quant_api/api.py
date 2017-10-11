#-*- coding:utf-8 -*-

import falcon

from stock import StockResource, StockAllResource, StockUtilResurce
from benchmark import BenchmarkResource, BenchmarkAllResource
from wsgiref import simple_server


app = falcon.API()

stock = StockResource()
stock_all = StockAllResource()
stock_util = StockUtilResurce()

benchmark_all = BenchmarkAllResource()
benchmark = BenchmarkResource()

app.add_route('/api/stocks', stock_all)
app.add_route('/api/stock/{stock_code}', stock)
app.add_route('/api/benchmark/all', benchmark_all)
app.add_route('/api/benchmark/{benchmark_name}', benchmark)
app.add_route('/api/stock/fields', stock_util)
