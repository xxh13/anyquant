#-*- coding:utf-8 -*-
__author__ = 'cheng'


import json
import datetime
import re
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta

from anyquant.api import get_pe, get_sha300_stocks, get_specified_stockinfo, get_stockcode

def api_pe(request):
    from datetime import datetime
    date = datetime(2013, 1, 4)
    return HttpResponse(json.dumps({'status': 'ok', 'data': get_pe('sh600000', date)}))

def api_sha300(request):
    from datetime import datetime

    date = datetime(2013, 6, 30)
    stocks = get_sha300_stocks(date)

    return HttpResponse(json.dumps({'status': 'ok', 'data': stocks, 'size': len(stocks)}))

def api_specified_stock(request, stock_code):
    """
    返回某个股票的历史日线行情数据
    :param request:{'stock_code': 股票代码,
                    'start_time': 查询的开始时间,
                    'end_time': 查询的结束时间}
    :return:{'status': 'ok', 'data':[{'date': 日期,
      'open': 开盘价,
      'high': 最高价,
      'close': 收盘价,
      'low': 最低价,
      'volume': 成交量,
      'adj_price': 后复权数据,
      'turnover': 换手率,
      'pe_ttm': 最近12个月的市盈率,
      'ps_ttm': 最近12个月的市销率,
      'pc_ttm': 最近12个月的市现率,
      'pb': 市净率,
      }]
      }
    """

    #默认使用半年作为时间跨度
    start_time = request.GET.get('start_time',str(datetime.date.today() + relativedelta(months=-6)))
    end_time = request.GET.get('end_time', str(datetime.date.today()))

    is_start_right = re.match(r'\d{4}-\d{2}-\d{2}', start_time)#匹配时间格式是否正确
    is_end_right = re.match(r'\d{4}-\d{2}-\d{2}', end_time)

    if((not is_start_right) or (not is_end_right)): #时间格式不正确，返回错误信息
        return HttpResponse(json.dumps({'status': 'error', 'data': [],
                                        'info': 'the date format is not right'}))

    stock_info_list = get_specified_stockinfo(stock_code, start_time, end_time)
    if(len(stock_info_list) == 0):
        return HttpResponse(json.dumps({'status': 'warning', 'data': stock_info_list,
                                        'info': 'data do not exist, please check your conditions' }))

    return HttpResponse(json.dumps({'status': 'ok', 'data': stock_info_list, 'info': 'ok'}))

def api_all_stockcode(request):
    """
    返回所有可用的股票代码
    :param
    :return :{'status': 'ok', 'data':[{'code': 股票代码}, {} ...]}
    """
    code_list = get_stockcode()
    return HttpResponse(json.dumps({'status': 'ok', 'data': code_list}))

