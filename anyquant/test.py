#-*- coding:utf-8 -*-
__author__ = 'cheng'

#from unittest import TestCase
from django.test import TestCase

from datetime import datetime
from api import get_pe, get_sha300_stocks

from quant_lab.models import StockSHA300

from datetime import datetime


class ApiTest(TestCase):

    def setUp(self):
        StockSHA300.objects.create(code='sh600000', name='test', date=datetime.now(), weight=0.12)
        StockSHA300.objects.create(code='sh600001', name='test2', date=datetime.now(), weight=0.11)
        StockSHA300.objects.create(code='sh600001', name='test2', date=datetime.now(), weight=0.13)

    def tet_api_get_pe(self):
        target_time = datetime(2013, 1, 4)

        print get_pe('sh600000', target_time)

    def test_get_sha300(self):

        stocks = get_sha300_stocks()

        print stocks


