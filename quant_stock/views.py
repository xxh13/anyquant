from django.shortcuts import render
from django.conf.urls import url
from django.http import HttpResponse
from models import StockInfo

# Create your views here.


def stock_index(request):
    # data = StockInfo.objects.filter("")
    return HttpResponse("hello index")


def stock_similar(request):
    return HttpResponse("hello similar")

stock_urls = (
    url(r'^api/stock/$', stock_index),
    url(r'^api/stock/similar/$', stock_similar)
)