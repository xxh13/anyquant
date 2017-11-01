from django.shortcuts import render
from django.conf.urls import url
from django.http import HttpResponse
from servies_model.similar_search.search_ts import search_similar

import json
from datetime import datetime

from models import StockData
from MyJson import MyJSONEncoder

# Create your views here.


def stock_index(request):
    # data = StockInfo.objects.filter("")
    return HttpResponse("hello index")


def stock_similar(request):
    """
    :param request:
    :return: {'status': 'ok', 'data' : [[], [], []]}
    method: post
    field: code trade_date, feature
    """
    if request.method != 'GET':
        return HttpResponse(json.dumps({'status': 'error'}))
    data = request.GET
    code = data.get('stock_code', None)
    trade_date = data.get('trade_date', None)
    feature = data.get('feature', 'close')
    if code is None:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'required param code are not passed'}))
    if trade_date is None:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'required param trade_date are not passed'}))
    try:
        trade_date = datetime.strptime(trade_date, '%Y-%m-%d').date()
    except Exception:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'invalid date format'}))
    dict_param = {'close': 0.6, 'open': 0.1, 'high': 0.1, 'low': 0.1, 'volume': 0.1}
    ok, result = search_similar(code, trade_date, feature, **dict_param)
    if not ok:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'no data'}))
    code_list = result[0]
    trade_date_list = result[1]
    return_data = [code_list, trade_date_list, []]
    for i in range(len(code_list)):
        stock_data = StockData.objects.filter(code=code_list[i],
                                            trade_date__gt=trade_date_list[i]).order_by('trade_date')[:1][0]
        return_data[2].append(stock_data.p_change)
    return HttpResponse(json.dumps({'status': 'ok', 'data': return_data}, cls=MyJSONEncoder))

stock_urls = (
    url(r'^api/stock/$', stock_index),
    url(r'^api/stock/similar/$', stock_similar)
)