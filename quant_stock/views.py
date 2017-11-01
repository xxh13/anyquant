from django.shortcuts import render
from django.conf.urls import url
from django.http import HttpResponse
from servies_model.similar_search.search_ts import search_similar

import json
from datetime import datetime

# Create your views here.


def stock_index(request):
    # data = StockInfo.objects.filter("")
    return HttpResponse("hello index")


def stock_similar(request):
    """
    :param request:
    :return:
    method: post
    field: code trade_date, feature
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({'status': 'error'}))
    data = request.POST
    code = data.get('code', None)
    trade_date = data.get('trade_date', None)
    feature = data.get('feature', 'close')
    if code is None:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'required param code are not passed'}))
    if trade_date is None:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'required param trade_date are not passed'}))
    try:
        trade_date = datetime.strptime(trade_date, '%Y-%m-%d')
    except Exception:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'invalid date format'}))
    dict = {'close': 0.6, 'open': 0.1, 'high': 0.1, 'low': 0.1, 'volume': 0.1}
    print 'das'
    ok, result = search_similar(code, trade_date, feature, dict)
    print ok
    if not ok:
        return HttpResponse(json.dumps({'status': 'ok', 'message': 'no data'}))
    print result
    return HttpResponse(json.dumps({'status': 'ok', 'data': result}))

stock_urls = (
    url(r'^api/stock/$', stock_index),
    url(r'^api/stock/similar/$', stock_similar)
)