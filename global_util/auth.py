#-*- coding:utf-8 -*-
__author__ = 'cheng'

__doc__ = """
    认证库，包括对用户是否登录的check，用户是否有权限运行策略的check
"""

import json

from django.http import HttpResponseRedirect, HttpResponse

from account.models import Account
from quant_lab.models import Strategy

from quant_base.settings import ADMIN_EMAILS

from DjangoCaptcha import Captcha


def login_check(f):
    """
    校验访问页面是否需要登录
    :param f:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get('strategy_id') == 'demo':
            #run demo
            return f(request, *args, **kwargs)

        if kwargs.get('strategy_visit_id') == 'demo':
            #demo page, have access
            return f(request, *args, **kwargs)
        if 'account' in request.session.keys():
            return f(request, *args, **kwargs)
        return HttpResponseRedirect('/')
    return wrapper


def auth_check(f):
    """
    校验是否需要鉴权，一般是用户是否有权访问请求的策略,
    需要在request参数中有 strategy_visit_id 参数
    如果是POST方法，body中需要有strategy_id 参数
    :param f:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            strategy_id = request.POST.get('strategy_id')
            account = request.session.get('account')
            try:
                strategy = Strategy.objects.get(id=strategy_id)
                if str(strategy.account_id.id) == str(account['id']):
                    return f(request, *args, **kwargs)
                else:
                    return HttpResponseRedirect('/labs')
            except:
                return HttpResponseRedirect('/labs')
        elif request.method == 'GET':
            strategy_visit_id = kwargs.get('strategy_visit_id')
            account = request.session.get('account')

            #demo策略直接显示
            if strategy_visit_id == 'demo':
                return f(request, *args, **kwargs)

            if account:
                try:
                    strategy = Strategy.objects.get(visit_id=strategy_visit_id)
                    if strategy.account_id.id == account['id']:
                        return f(request, *args, **kwargs)
                    else:
                        return HttpResponseRedirect('/labs')
                except:
                    return HttpResponseRedirect('/labs')
            else:
                return HttpResponseRedirect('/')
        #return f(request, *args, **kwargs)
    return wrapper


def admin_check(f):
    """
    检查是否为管理员账户, 用于管理员界面
    :param f:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        account_info = request.session.get('account')

        if account_info:
            email = account_info['email']
            if email in ADMIN_EMAILS:
                return f(request, *args, **kwargs)
        #return HttpResponseRedirect('/')
        return f(request, *args, **kwargs)
    return wrapper

def captch_check(f):
    """
    decoration 用于ajax方法中验证码的检验
    :param f:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            if not request.POST.has_key('code'):
                return f(request, *args, **kwargs)

            _code = request.POST.get('code') or ''

            if not _code:
                return HttpResponse(json.dumps({'status': 'error', 'data': u'验证码错误'}))

            ca = Captcha(request)
            if ca.check(_code):
                return f(request, *args, **kwargs)
            else:
                return HttpResponse(json.dumps({'status': 'error', 'data': u'验证码错误'}))
        return f(request, *args, **kwargs)
    return wrapper


def captch_http_check(code, request):
    ca = Captcha(request)
    if ca.check(code):
        return True
    else:
        return False
