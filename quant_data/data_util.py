# -*- coding: utf-8 -*-

from quant_lab.models import Stock, StockSHA300
from django.http import HttpResponse
import json
from datetime import datetime, timedelta


def get_stock_sha300_code():
    """
    返回300成分股的代码编号
    :return: stock_return[]
    """
    stock_return = []
    stock_sha300_objects = StockSHA300.objects.all().values('code').distinct()
    for stock_sha300 in stock_sha300_objects:
        stock_return.append(stock_sha300['code'])

    return stock_return


def get_stocks_count():
    return Stock.objects.values('code').distinct().count()


def get_max_date_stock(stock_type, start, end):
    """
    获取股票
    :param stock_type:
    :param start:
    :param end:
    :return:
    """

    if stock_type == 11:
        stock_sha300 = get_stock_sha300_code()
        stock_max_date = Stock.objects.filter(code__in=stock_sha300).order_by('-date')[start: end]
    else:
        stock_max_date = Stock.objects.all().order_by('-date')[start: end]

    return stock_max_date



