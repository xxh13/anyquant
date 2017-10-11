# -*-coding:utf-8 -*-
"""
    一些辅助处理的函数
"""

from settings import DATABASES, FIELDS_BASE, FIELDS_SENIOR
from model import Stock, Stock_info
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, distinct ,func, and_, Column
import datetime


# 帮助获取对应的股票号码函数
def get_stock_code(start, exchange):
    to_return_info = []
    engine = create_engine('mysql+mysqldb://'+ DATABASES['default']['USER'] + ':' + DATABASES['default']['PASSWORD']
    + '@' + DATABASES['default']['HOST'] + ':' + DATABASES['default']['PORT'] + '/' + DATABASES['default']['NAME'])
    Session = sessionmaker(bind=engine)
    end = start + datetime.timedelta(days=365)
    for ex in exchange:
        to_return_info += list(Session().query(func.distinct(Stock.s_code))
                .filter(Stock.s_code.like(ex + '%'), Stock.s_date > start, Stock.s_date < end).limit(2000))
    return to_return_info


# 帮助获取特定股票信息函数
def get_stock_data(stock_code, start, end, fields):
    engine = create_engine('mysql+mysqldb://'+ DATABASES['default']['USER'] + ':' + DATABASES['default']['PASSWORD']
    + '@' + DATABASES['default']['HOST'] + ':' + DATABASES['default']['PORT'] + '/' + DATABASES['default']['NAME'])
    Session = sessionmaker(bind=engine)

    fields_base = ['date']
    fields_senior = ['date']
    for field in fields:
        if field in FIELDS_BASE:
            fields_base.append(field)
        if field in FIELDS_SENIOR:
            fields_senior.append(field)

    stock_info_base = list(Session().query(Stock).filter(and_(
        Stock.s_date > start, Stock.s_date < end, Stock.s_code == stock_code))\
        .order_by(Stock.s_date).values(*fields_base))
    stock_info_senior = list(Session().query(Stock_info).filter(and_(
        Stock_info.s_date > start, Stock_info.s_date < end, Stock_info.s_code == stock_code))\
        .order_by(Stock_info.s_date).values(*fields_senior))

    to_return_info = []
    index = 0
    for i in range(len(stock_info_base)):
        data = {}
        data['date'] = stock_info_base[i][0].strftime('%Y-%m-%d')
        for m in range(len(fields_base))[1:]:
            data[fields_base[m]] = stock_info_base[i][m]
        if stock_info_base[i][0] == stock_info_senior[index][0]: 
            for n in range(len(fields_senior))[1:]:
                data[fields_senior[n]] = stock_info_senior[index][n]
            index += 1
        else:
            for n in range(len(fields_senior))[1:]:
                data[fields_senior[n]] = ''
        to_return_info.append(data)
    return to_return_info

# 帮助获取指定大盘指数
def get_benchmark_data(benchmark_name, start, end, fields):
    engine = create_engine('mysql+mysqldb://'+ DATABASES['default']['USER'] + ':' + DATABASES['default']['PASSWORD']
    + '@' + DATABASES['default']['HOST'] + ':' + DATABASES['default']['PORT'] + '/' + DATABASES['default']['NAME'])
    Session = sessionmaker(bind=engine)

    fields_base = ['date']
    fields_senior = ['date']
    for field in fields:
        if field in FIELDS_BASE:
            fields_base.append(field)
        if field in FIELDS_SENIOR:
            fields_senior.append(field)
            
    stock_info_base = list(Session().query(Stock).filter(and_(
        Stock.s_date > start, Stock.s_date < end, Stock.s_code == benchmark_name))\
        .order_by(Stock.s_date).values(*fields_base))
    stock_info_senior = list(Session().query(Stock_info).filter(and_(
        Stock_info.s_date > start, Stock_info.s_date < end, Stock_info.s_code == benchmark_name))\
        .order_by(Stock_info.s_date).values(*fields_senior))

    to_return_info = []
    index = 0
    for i in range(len(stock_info_base)):
        data = {}
        data['date'] = stock_info_base[i][0].strftime('%Y-%m-%d')
        for m in range(len(fields_base))[1:]:
            data[fields_base[m]] = stock_info_base[i][m]
        if len(stock_info_senior) > 0:
            if stock_info_base[i][0] == stock_info_senior[index][0]: 
                for n in range(len(fields_senior))[1:]:
                    data[fields_senior[n]] = stock_info_senior[index][n]
                index += 1
            else:
                for n in range(len(fields_senior))[1:]:
                    data[fields_senior[n]] = ''
        to_return_info.append(data)
    return to_return_info