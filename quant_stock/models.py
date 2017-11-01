# -*- coding:utf-8 -*-

from django.db import models


# 股票代码信息
class StockInfo(models.Model):
    id = models.AutoField(primary_key=True)

    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    aggrv = models.CharField(max_length=100) # 中文首字母
    spell = models.CharField(max_length=100) # 中文全拼

    class Meta:
        verbose_name = 'stocks_info'


class StockData(models.Model):
    id = models.AutoField(primary_key=True)

    code = models.CharField('code', max_length=100)
    open = models.FloatField('open', max_length=10)
    close = models.FloatField('close', max_length=10)
    high = models.FloatField('high', max_length=10)
    low = models.FloatField('low', max_length=10)
    trade_date = models.DateField('trade_date')
    volume = models.IntegerField('volume', max_length=10)
    price_change = models.FloatField('price_change', max_length=10)
    p_change = models.FloatField('p_change', max_length=10)
    ma5 = models.FloatField('ma5', max_length=10)
    ma10 = models.FloatField('ma10', max_length=10)
    ma20 = models.FloatField('ma20', max_length=10)
