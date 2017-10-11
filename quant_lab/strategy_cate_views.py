#-*- coding:utf-8 -*-

import json
import pytz
from datetime import datetime
from hashlib import md5

from django.http import HttpResponse

from models import Strategy, StockSHA300, StrategyCateData, StrategyCate
from account.models import Account

from quant_lab_util import check_category_valid

from global_util.auth import login_check


###策略分类信息
@login_check
def strategy_cate_new(request):
    """
    创建策略分类 /strategy/cate/new
    :param request: {'name': ''}
    :return: {'status': 'ok', 'data': '', 'category': {'name': '', 'visit_id': '', 'id': ''}}
    """
    if request.method == 'POST':
        account = request.session.get('account')
        cate_name = request.POST.get('name')

        if not check_category_valid(cate_name, account['id']):
            return HttpResponse(json.dumps({'status': 'error', 'data': u'分类名字非法，请换一个'}))

        s_c = StrategyCate(name=cate_name, account_id=Account.objects.get(id=account['id']))
        s_c.date = datetime.now(tz=pytz.UTC)
        s_c.visit_code = md5(str(account['id']) + cate_name.encode('utf-8') +
                             datetime.now().strftime("%Y%m%d%H%M%S")).hexdigest()[:8]

        try:
            s_c.save()
            return HttpResponse(json.dumps({'status': 'ok', 'data': u'创建分类成功',
                    'category': {'name': s_c.name, 'visit_id': s_c.visit_code, 'id': s_c.id}}))
        except Exception, e:
            return HttpResponse(json.dumps({'status': 'error', 'data': '创建分类失败，请稍后再试'}))
    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))


@login_check
def strategy_cate_update(request):
    """
    修改策略分组信息 /strategy/cate/updtae
    :param request: {'name': '' #new name, 'id': '' #cate id}
    :return: {'status': '', 'data': '', 'category': {'name': '', 'visit_id': '', 'id': ''}}
    """
    if request.method == 'POST':
        account = request.session.get('account')
        new_name = request.POST.get('name')
        cate_id = request.POST.get('id')

        if not check_category_valid(new_name, account['id']):
            return HttpResponse(json.dumps({'status': 'error', 'data': u'分类名非法'}))

        try:
            s_c = StrategyCate.objects.get(account_id__id=account['id'], id=cate_id)
            s_c.name = new_name
            s_c.date = datetime.now(tz=pytz.UTC)
            s_c.visit_code = md5(str(account['id']) + new_name.encode('utf-8') +
                             datetime.now().strftime("%Y%m%d%H%M%S")).hexdigest()[:8]
            s_c.save()
            return HttpResponse(json.dumps({'status': 'ok', 'data': u'修改分组信息成功',
                    'category': {'name': s_c.name, 'visit_id': s_c.visit_code, 'id': s_c.id}}))
        except:
            return HttpResponse(json.dumps({'status': 'error', 'data': u'修改分组信息失败'}))
    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))


@login_check
def strategy_cate_remove(request):
    """
    删除策略分组 /strategy/cate/remove
    :param request: {‘id’: ''}
    :return:
    """
    if request.method == 'POST':
        cate_id = request.POST.get('id')
        account = request.session.get('account')

        try:
            #删除分组下的所有记录
            StrategyCateData.objects.filter(account_id__id=account['id'],
                                            strategy_cate_id__id=cate_id).delete()
            #删除分组信息
            StrategyCate.objects.get(account_id__id=account['id'], id=cate_id).delete()
            return HttpResponse(json.dumps({'status': 'ok', 'data': u'删除成功'}))
        except:
            return HttpResponse(json.dumps({'status': 'error', 'data': u'删除失败'}))
    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))


@login_check
def strategy_cate_strategy_move(request):
    """
    修改策略所属分类信息
    :param request: {'strategy_id': '', 'cate_id': ''}
    :return:
    """
    if request.method == 'POST':
        strategy_id = request.POST.get('strategy_id')
        cate_id = request.POST.get('cate_id')
        account = request.session.get('account')

        if str(cate_id) == '-1':
            #策略分类设回默认，删除记录
            StrategyCateData.objects.filter(account_id__id=account['id'],
                                            strategy_id__id=strategy_id).delete()

            return HttpResponse(json.dumps({'status': 'ok', 'data': u'修改策略分组成功'}))

        if len(StrategyCateData.objects.filter(account_id__id=account['id'],
                                               strategy_id__id=strategy_id)) == 0:
            #说明是策略之前没分组记录,新加即可
            try:
                strategy = Strategy.objects.get(id=strategy_id)
                if strategy.account_id.id != int(account['id']):
                    return HttpResponse(json.dumps({'status': 'error', 'data': u'策略账号不符'}))
                strategy_cate_data = StrategyCateData(strategy_id=strategy,
                                                      account_id=strategy.account_id,
                                                      strategy_cate_id=StrategyCate.objects.get(id=cate_id))
                strategy_cate_data.save()
                return HttpResponse(json.dumps({'status': 'ok', 'data': u'修改策略分组成功'}))
            except:
                return HttpResponse(json.dumps({'status': 'error', 'data': u'修改策略分组失败'}))

        try:
            strategy_cate_data = StrategyCateData.objects.get(account_id__id=account['id'],
                                                              strategy_id__id=strategy_id)
            strategy_cate_data.strategy_cate_id = StrategyCate.objects.get(id=cate_id)
            strategy_cate_data.save()
            return HttpResponse(json.dumps({'status': 'ok', 'data': u'修改策略分组成功'}))
        except:
            return HttpResponse(json.dumps({'status': 'error', 'data': u'修改策略分组错误'}))
    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))