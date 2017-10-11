#-*- coding:utf-8 -*-
__author__ = 'cheng'

from hashlib import md5
from django.db import models


class Stock(models.Model):
    id = models.AutoField(primary_key=True)

    type = models.IntegerField()    #1 a股 11 sha300 成分股
    code = models.CharField(max_length=100)
    date = models.DateTimeField()

    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    adj_price = models.FloatField()

    volume = models.BigIntegerField()

    class Meta:
        db_table = 'stocks'


class StockInfo(models.Model):
    id = models.AutoField(primary_key=True)

    type = models.IntegerField()
    code = models.CharField(max_length=100)
    date = models.DateTimeField()

    turnover = models.FloatField()  #换手率 成交量、流通股本
    pe_ttm = models.FloatField()    #最近12个月的市盈率
    ps_ttm = models.FloatField()    #最近12个月的市销率
    pc_ttm = models.FloatField()    #最近12个月的市现率
    pb = models.FloatField()    #市净率

    class Meta:
        db_table = 'stock_info'


class StockSHA300(models.Model):
    #沪深300成分股
    id = models.AutoField(primary_key=True)

    code = models.CharField(max_length=100) #股票代码
    name = models.CharField(max_length=100) #股票简称

    date = models.DateTimeField()   #统计日期

    weight = models.FloatField()    #股票权重

    class Meta:
        db_table = 'stock_sha300'

class Strategy(models.Model):
    """
    策略文件保存，一个账号有多个策略
    """
    id = models.AutoField(primary_key=True)
    visit_id = models.CharField(max_length=50, default='')

    account_id = models.ForeignKey('account.Account', db_column='account_id')
    name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    capital_base = models.FloatField()
    freq = models.CharField(max_length=10)

    class Meta:
        db_table = 'strategy'


class StrategyIns(models.Model):
    """
    策略运行实例保存
    """
    id = models.AutoField(primary_key=True)

    account_id = models.ForeignKey('account.Account', db_column='account_id')
    strategy_id = models.ForeignKey('Strategy', db_column='strategy_id')
    file_path = models.CharField(max_length=200)

    date = models.DateTimeField()
    result = models.TextField(max_length=1024)
    info = models.TextField(max_length=1024)

    class Meta:
        db_table = 'strategy_ins'


class StrategyCate(models.Model):
    """
    策略分类元数据信息
    """
    id = models.AutoField(primary_key=True)

    account_id = models.ForeignKey('account.Account', db_column='account_id')
    name = models.CharField(max_length=100)
    visit_code = models.CharField(max_length=100)
    date = models.DateTimeField()

    class Meta:
        db_table = 'strategy_cate'


class StrategyCateData(models.Model):
    """
    策略分类存储数据，策略，分类多对多关系
    """
    id = models.AutoField(primary_key=True)

    strategy_id = models.ForeignKey('Strategy', db_column='strategy_id')

    strategy_cate_id = models.ForeignKey('StrategyCate', db_column='strategy_cate_id')

    account_id = models.ForeignKey('account.Account', db_column='account_id')

    class Meta:
        db_table = 'strategy_cate_data'