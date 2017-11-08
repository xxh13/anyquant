# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'id', primary_key=True)),
                ('code', models.CharField(max_length=100, verbose_name=b'code')),
                ('open', models.FloatField(max_length=10, verbose_name=b'open')),
                ('close', models.FloatField(max_length=10, verbose_name=b'close')),
                ('high', models.FloatField(max_length=10, verbose_name=b'high')),
                ('low', models.FloatField(max_length=10, verbose_name=b'low')),
                ('trade_date', models.DateField(verbose_name=b'trade_date')),
                ('volume', models.IntegerField(verbose_name=b'volume')),
                ('price_change', models.FloatField(max_length=10, verbose_name=b'price_change')),
                ('p_change', models.FloatField(max_length=10, verbose_name=b'p_change')),
                ('ma5', models.FloatField(max_length=10, verbose_name=b'ma5')),
                ('ma10', models.FloatField(max_length=10, verbose_name=b'ma10')),
                ('ma20', models.FloatField(max_length=10, verbose_name=b'ma20')),
                ('v_ma5', models.FloatField(max_length=10, verbose_name=b'v_ma5')),
                ('v_ma10', models.FloatField(max_length=10, verbose_name=b'v_ma10')),
                ('v_ma20', models.FloatField(max_length=10, verbose_name=b'v_ma20')),
                ('turnover', models.FloatField(max_length=10, verbose_name=b'turnover')),
            ],
            options={
                'db_table': 'stock_data',
                'verbose_name': 'stock_data',
            },
        ),
        migrations.CreateModel(
            name='StockInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'id', primary_key=True)),
                ('code', models.CharField(max_length=100, verbose_name=b'code')),
                ('name', models.CharField(max_length=100, verbose_name=b'name')),
                ('aggrv', models.CharField(max_length=100, verbose_name=b'aggrv')),
                ('spell', models.CharField(max_length=100, verbose_name=b'spell')),
            ],
            options={
                'db_table': 'stocks_info',
                'verbose_name': 'stocks_info',
            },
        ),
    ]
