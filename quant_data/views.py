# -*- coding:utf-8 -*-
# 获取历史数据


from quant_base.settings import STOCK_PER_PAGE
from quant_lab.models import Stock, StockInfo, StockSHA300
from data_util import get_max_date_stock, get_stocks_count

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.db.models import Q, Max
import math
import pytz
import json


# 显示所有股票的最新的历史数据，用于数据首页
def stock_data_all(request):
    """
    股票数据首页,默认是所有A股
    :param request: type(default 11)
    :return:{'status': '' , 'data': 'stock': {['id': '', ''code': '', 'open': '', 'high': '', 'low': '',
                                     'close': '', 'adj_price': '', 'volume': '', 'name': '', 'date': ''],
                                     'page': '', 'total_pages': ''}}'
    """
    to_return_info = {'status': 'ok', 'data': {}}

    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        if page < 0:
            page = 1

        try:
            stock_type = int(request.GET.get('type', '1'))
        except:
            stock_type = 1

        if type != 1 or type != 11:
            stock_type = 1

        stock_num = get_stocks_count()

        if (page - 1) * STOCK_PER_PAGE > stock_num:
            page = 1

        stock_filter = get_max_date_stock(stock_type, (page-1)*STOCK_PER_PAGE, page*STOCK_PER_PAGE)

        stock_sha300_objects = StockSHA300.objects

        stock_list = []

        for stock in stock_filter:
            stock_info = {'id': stock.id, 'code': stock.code, 'open': stock.open, 'high': stock.high,
                          'low': stock.low, 'close': stock.close, 'adj_price': stock.adj_price,
                          'name': '--', 'volume': stock.volume, 'date': stock.date.strftime("%Y-%m-%d")}

            stock_sha300 = stock_sha300_objects.filter(code=stock.code)
            if len(stock_sha300) > 0:
                stock_info['name'] = stock_sha300[0].name
            stock_list.append(stock_info)

        to_return_info['data']['stock'] = stock_list
        to_return_info['data']['page'] = page
        to_return_info['data']['total_pages'] = int(math.ceil(stock_num * 1.0 / STOCK_PER_PAGE)) \
            if stock_num > 0 else 1

        return render_to_response('quant_data/history.html', to_return_info, RequestContext(request))


# 显示股票基本数据
def stock_detail_basic(request):
    """
    输入代码的code显示历史数据
    :param request: 'start':'' ,'end': '',code: '', page: ''
    :return:{'status': '', 'data': 'stock': [{'id':'',  'date':'', 'open':'', 'high':'','name': ''
                                    'low':'', 'close':'', 'adj_price':'', 'volume':''}],
                                    'start': '', 'end': '', 'page': '', total_pages': '','code':'' ,}
    """
    to_return_info = {'status': 'ok', 'data': {}}
    date_format = '%Y-%m-%d'
    default_start = timezone.now() - timedelta(days=365)
    default_end = timezone.now()

    if request.method == 'GET':
        code = request.GET.get('code', '')
        start = request.GET.get('start', datetime.strftime(default_start, date_format))
        end = request.GET.get('end', datetime.strftime(default_end, date_format))

        try:
            page = int(request.GET.get('page', 1))
        except :
            page = 1

        if page < 0:
            page = 1

        try:
            stocks_object = Stock.objects.filter(Q(code=code) & Q(date__range=(start, end))).order_by('-date')

            stock_sha300 = StockSHA300.objects.filter(code=code)

            if (page-1)*STOCK_PER_PAGE > len(stocks_object):
                page = 1

            stocks_filter = stocks_object[(page-1)*STOCK_PER_PAGE: page*STOCK_PER_PAGE]

            stock_list = []
            for stock in stocks_filter:
                stock_list.append({'id': stock.id, 'date': stock.date.strftime("%Y-%m-%d"),
                                   'open': stock.open, 'high': stock.high, 'low': stock.close,
                                   'close': stock.close, 'adj_price': stock.adj_price, 'volume': stock.volume})
            to_return_info['data']['stock'] = stock_list

            to_return_info['data']['code'] = code
            to_return_info['data']['name'] = stock_sha300[0].name if len(stock_sha300) > 0 else '--'
            to_return_info['data']['start'] = start
            to_return_info['data']['end'] = end
            to_return_info['data']['page'] = page
            to_return_info['data']['total_pages'] = int(math.ceil(len(stocks_object) * 1.0 / STOCK_PER_PAGE))\
                if len(stocks_object) > 0 else 1

            return render_to_response('quant_data/history_detail.html', to_return_info, RequestContext(request))
        except:
            return redirect('/stock/history_data')
    else:
        return redirect('/stock/history_data')
