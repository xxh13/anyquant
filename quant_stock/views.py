import json
from datetime import datetime

from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render_to_response

from models import StockData, StockInfo
from servies_model.similar_search.search_ts import search_similar
from util.MyJson import MyJSONEncoder


# Create your views here.


def stock_index(request):
    # data = StockInfo.objects.filter("")
    return render_to_response('data_service/service_home.html', {})


def stock_similar_home(request):
    return render_to_response('data_service/similar_analysis.html', {})


def stock_similar(request):
    """
    :param request:
    :return: {'status': 'ok', 'data' : [[], [], []]}
    method: post
    field: code trade_date, feature
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({'status': 'error'}))
    data = request.POST
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
    return_data = {'status': 'ok', 'code': code_list, 'date': trade_date_list, 'scope': []}
    for i in range(len(code_list)):
        stock_data = StockData.objects.filter(code=code_list[i],
                                              trade_date__gt=trade_date_list[i]).order_by('trade_date')[:1][0]
        return_data['scope'].append(stock_data.p_change)
    return HttpResponse(json.dumps(return_data, cls=MyJSONEncoder))


def complete_stock(request):
    """
    :param request:
    :return:
    """
    if request.method != 'GET':
        return HttpResponse(json.dumps({'status': 'error'}))
    prefix = request.GET.get('prefix', None)
    limit = request.GET.get('limit', 100)
    if prefix is None:
        stock_info = StockInfo.objects.filter()
    else:
        if '0' <= prefix[0] <= '9':
            stock_info = StockInfo.objects.filter(code__startswith=prefix)
        elif u'\u4e00' <= prefix[0] <= prefix[0] <= u'\u9fbb':
            stock_info = StockInfo.objects.filter(name__startswith=prefix)
        elif 'A' <= prefix[0] <= 'Z' or 'a' <= prefix <= 'z':
            try:
                stock_info = StockInfo.objects.filter(aggrv__startswith=str(prefix).upper())
            except Exception as e:
                return HttpResponse(json.dumps({'status': 'error', 'message': 'invalid format'}))
        else:
            return HttpResponse(json.dumps({'status': 'error', 'message': 'invalid format'}))
    stock_filter_info = map(lambda x: {'code': x.code, 'name': x.name, 'aggrv': x.aggrv}, stock_info)
    return_data = {'status': 'ok', 'data': stock_filter_info[:limit]}
    return HttpResponse(json.dumps(return_data))


stock_urls = (
    url(r'^service/$', stock_index),
    url(r'^service/similar_analysis/$', stock_similar_home),
    url(r'^api/stock/similar/$', stock_similar),
    url(r'^api/stock/complete', complete_stock)
)