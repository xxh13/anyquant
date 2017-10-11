#-*- coding:utf-8 -*-


__author__ = 'cheng'

from dateutil.relativedelta import relativedelta

from quant_lab.models import StockInfo, StockSHA300, Stock
from django.db import connection
"""
any quant api
called by trading strategy
"""

def get_sha300_stocks(date=None):
    """
    get sha300 stocks given date
    :param date:
    :return:
    """
    if date is not None:
        start_date = date
        end_date = date + relativedelta(months=6) #默认使用半年作为时间跨度，如果后面成分股更新，需更新
        all_stocks = StockSHA300.objects.filter(date__gte=date).filter(date__lt=end_date).all()
        return [stock.code for stock in all_stocks]
    else:
        #返回历史所有成分股
        all_stocks = StockSHA300.objects.values('code').distinct()

        return [stock['code'] for stock in all_stocks]


def get_pe(symbol, date):
    """
    return PE data given stock symbol
    :param symbol:
    :return:
    """
    stock_info = StockInfo.objects.filter(code=symbol).filter(date=date).all()

    if stock_info:
        target_info = stock_info[0]

        return target_info.pe_ttm

    return 0.0

def get_specified_stockinfo(stock_code, start_time, end_time):
    """
    返回某个股票的历史日线行情数据
    :param stock_code:股票代码
    :param start_time:查询的开始时间
    :param end_time:查询的结束时间
    :return:[{'date': 日期,结果按照日期降序排列
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
    """
    #查询stocks 和 stockinfo 表
    raw_sql = "select s.date,s.open,s.high,s.close,s.low,s.volume," \
              "s.adj_price,si.turnover,si.pe_ttm,si.ps_ttm,si.pc_ttm,si.pb" \
              " from stocks s, stock_info si " \
              "where s.code=si.code and s.code=%s " \
                "and s.date>=%s and s.date<=%s " \
                "and s.date=si.date" \
              " order by s.date desc"
    cursor=connection.cursor()
    cursor.execute(raw_sql, [stock_code, start_time, end_time])
    stock_set = cursor.fetchall()
    stock_info_list = [{'date': str(stock[0].strftime("%Y-%m-%d")),
      'open': stock[1],
      'high': stock[2],
      'close': stock[3],
      'low': stock[4],
      'volume': stock[5],
      'adj_price': stock[6],
      'turnover': stock[7],
      'pe_ttm': stock[8],
      'ps_ttm': stock[9],
      'pc_ttm': stock[10],
      'pb': stock[11],
      } for stock in stock_set]
    return stock_info_list

def get_stockcode():
    """
    返回所有可用的股票代码
    :param
    :return :[{'code': 股票代码}, {} ...]
    """
    stockcode_set = Stock.objects.values('code').distinct()
    code_list = [{'code': code['code']} for code in stockcode_set]
    return code_list

