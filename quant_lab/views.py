#-*- coding:utf-8 -*-
__author__ = 'cheng'

import json
import jedi
from datetime import datetime, timedelta
from hashlib import md5
import logging
import math
import pytz

from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext

from models import Strategy, StockSHA300, StrategyCate, StrategyIns, StrategyCateData

from code_exec import execute_code
from quant_lab_util import get_strategy_info, \
    save_code_file, save_code_ins_file, save_strategy_ins, \
    save_strategy as s_strategy, get_filter_strategy_list, \
    get_current_category, get_category_info_by_strategy
from quant_base.settings import CODE_DIR

from global_util.auth import auth_check, login_check
from quant_base.settings import STRATEGY_PER_PAGE


log = logging.getLogger('custom')


def home(request):
    """
    /labs[?page=1&cate=<visit_id> default/]
    我的策略,需要获取当前账号下所有的策略
    :param request:
    :return: {'strategy_category': [{‘name’: '', 'visit_id': '', 'id': '', 'active': 1}],
            'current_category': {'name': '所有/默认', 'visit_id': '', 'id': ''},
        'strategy': [{'name': '', 'id': '',  'start': '', 'end': '', 'strategy_category': '', 'strategy_cate_id': ''}],
            'page': 1,
            'total_pages': 2}
    """
    account = request.session.get('account', None)
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    all_strategy_objects = []
    all_strategy = []
    all_strategy_cate_list = []
    cate = request.GET.get('cate')
    if account is not None:
        all_strategy_cate_list = StrategyCate.objects.filter(account_id__id=account['id'])

        #根据分类过滤,如果参数 cate = <visit_code>， default则为default cate=default, 没有则为全部查询
        all_strategy_objects = get_filter_strategy_list(account['id'], cate)

        cur_page_strategy_list = all_strategy_objects[(page - 1) * STRATEGY_PER_PAGE: page * STRATEGY_PER_PAGE]

        for s in cur_page_strategy_list:
            strategy_cate_info = get_category_info_by_strategy(s.id)
            all_strategy.append({'name': s.name, 'id': s.id, 'visit_id': s.visit_id,
                         'start': s.start, 'end': s.end, 'strategy_category': strategy_cate_info['name'],
                         'strategy_cate_id': strategy_cate_info['id']})

    return render_to_response('quant_lab/lab_home.html',
                              {'strategy_category': [{'name': s_c.name,
                                                       'visit_id': s_c.visit_code,
                                                       'id': s_c.id} for s_c in all_strategy_cate_list],
                               'current_category': get_current_category(account.get('id') if account else None, cate),
                               'strategy': all_strategy,
                               'page': page,
                               'total_pages': int(math.ceil(len(all_strategy_objects) * 1.0 / STRATEGY_PER_PAGE)) \
            if len(all_strategy_objects) > 0 else 1}, RequestContext(request))


@login_check
def new_strategy(request):
    """
    /strategy/new
    创建新的策略文件,默认直接返回初始代码，不可配置
    成功后直接跳转到编辑页面
    :param request: POST {'name': ''}
    :return:
    """
    if request.method == 'POST':
        name = request.POST.get('strategy_name')

        if len(Strategy.objects.filter(name=name)) > 0:
                return HttpResponse(json.dumps({'status': 'error', 'data': u'策略名已存在！'}))

        start = (datetime.now(tz=pytz.UTC) + timedelta(days=-14)).strftime('%Y-%m-%d')
        end = (datetime.now(tz=pytz.UTC) + timedelta(days=-7)).strftime('%Y-%m-%d')
        visit_id = md5(name.encode('utf-8') + str(request.session.get('account')['id'])
                             + str(datetime.now().strftime("%Y%m%d%H%M%S"))).hexdigest()

        try:
            result_info = s_strategy(account_id=request.session.get('account')['id'], strategy_id=None,
                   code=None, params={'name': name, 'start': start, 'end': end,
                                      'capital_base': 100000, 'freq': u'每天', 'visit_id': visit_id})
            return HttpResponse(json.dumps(result_info))
        except Exception, e:
            log.error('==============Quant New Strategy Error: ', e)
            return HttpResponse(json.dumps({'status': 'error', 'data': u'系统出现错误，请稍后再试!'}))
    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))


def index(request):
    return render_to_response("index.html", {})


@login_check
def save_strategy(request):
    """
    ajax方法， 保存策略
    :param request: {'code': '',
    'params': {'start': '', 'end': '',
            'capital_base': '', 'freq': ''}} #account在session中
    :return: {'statuc': 'ok'}
    """
    if request.method == 'POST':
        code = request.POST.get('code')
        params = request.POST.get('params')
        strategy_id = request.POST.get('strategy_id')

        account_info = request.session.get('account')

        save_code_file(account_info['id'], strategy_id=strategy_id, code=code)

        return HttpResponse(json.dumps({'status': 'ok'}))


@login_check
def delete_strategy(request):
    """
    删除策略
    包括删除策略和策略运行实例，策略所属分类记录也要删除
    :param request: {'id': '<strategy_id>'}
    :return: {'status: 'ok/error', 'data': ''}
    """
    if request.method == 'POST':
        strategy_id = request.POST.get('id')
        account = request.session.get('account')

        #需要删除策略运行实例，分类记录，策略
        try:
            StrategyIns.objects.filter(account_id__id=account['id'], strategy_id__id=strategy_id).delete()
            StrategyCateData.objects.filter(account_id__id=account['id'], strategy_id__id=strategy_id).delete()
            Strategy.objects.filter(account_id__id=account['id'], id=strategy_id).delete()

            return HttpResponse(json.dumps({'status': 'ok', 'data': u'删除成功'}))
        except:
            return HttpResponse(json.dumps({'status': 'error', 'data': u'删除失败'}))

    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))


@login_check
@auth_check
def labs(request, strategy_visit_id):
    '''
    /labs/strategy/hash<<strategy_id>>
    算法编写首页
    :param request:
    :return: {'code': code, 'account': {'name': '', 'id': ''},
        'strategy_id': '', 'strategy_name': '',
        'params': {'start': '', 'end': '', 'capital_base': '', 'freq': ''}}
    '''
    #读取状态数据,如果没有登录，直接跳转到初始代码页面
    account_info = request.session.get('account')

    if account_info is None or strategy_visit_id == 'demo':
        #读取初始化代码
        with open(CODE_DIR + '/code_init.py', 'rb') as code_init_file:
            init_code = ''.join(code_init_file.readlines())

        return render_to_response("quant_lab/labs.html", {'code': init_code,
                    'strategy_id': 'demo',
                    'strategy_name': '演示策略',
                    'params': {'start': '2014-01-01', 'end': '2015-01-01', 'capital_base': '200000', 'freq': u'每天'}},
                    RequestContext(request))

    strategy_info = get_strategy_info(strategy_visit_id=strategy_visit_id, account_id=account_info['id'])
    to_return_info = {'code': strategy_info['code'],
                      'strategy_id': strategy_info['id'],
                      'strategy_name': strategy_info['name'],
                      'params': {'start': strategy_info['start'],
                                 'end': strategy_info['end'],
                                 'capital_base': strategy_info['capital_base'],
                                 'freq': strategy_info['freq']}}
    return render_to_response('quant_lab/labs.html', to_return_info, RequestContext(request))


@login_check
def run_algo(request):
    """
    运行算法，ajax方法
    :param request: code start end capital_base freq
    :return: 运行后的数据，{'data': {}, 'status': ''}
    annualized_return 年化收益率
    benchmark_annualized_return 基准年化收益率
    alpha 阿尔法
    beta 贝塔
    sharpe 夏普比率
    volatility 收益波动率
    information 信息比率
    max_drawdown 最大回撤
    cumulative_return: {'': 1} 策略累计收益率
    benchmark_ cumulative_return {'': 1} 基准累计收益率
    """
    if request.method == 'POST':
        account_info = request.session.get('account')

        code = request.POST.get('code')
        start_date = request.POST.get('start', '2013-02-01')
        end_date = request.POST.get('end', '2013-03-01')
        capital_base = request.POST.get('capital_base', 100000)
        freq = request.POST.get('freq', 'daily')
        strategy_id = request.POST.get('strategy_id', 0)
        #如果是登录用户，保存策略实例代码
        code_ins_path = None
        if account_info and strategy_id != 'demo':
            s_strategy(account_id=account_info['id'],
                       strategy_id=strategy_id, code=code,
                       params={'start': start_date, 'end': end_date,
                               'capital_base': capital_base, 'freq': freq})

            code_ins_path = save_code_ins_file(account_info['id'], strategy_id, code)

        #运行代码
        to_return_info = execute_code(code=code, capital_base=capital_base,
                     start=start_date, end=end_date, freq=freq, code_ins_path=code_ins_path)

        if account_info and strategy_id != 'demo':
            #运行实例保存
            save_strategy_ins(account_info['id'], strategy_id, code_ins_path, to_return_info, to_return_info)

    return HttpResponse(json.dumps(to_return_info))


def quant_help(request):
    return render_to_response('help.html', {})


@login_check
def quant_template_save(request):
    """
    模板配置保存, POST方法，
    :param request: {'name': '', start: 'YYYY-mm-dd', end: '',
        'capital_base': 100000, 'freq': '', code: ''}
    :return:
    """
    if request.method == 'POST':
        name = request.POST.get('name', u'示例模板股票策略')
        start = request.POST.get('start')
        end = request.POST.get('end')
        capital_base = request.POST.get('capital_base')
        freq = request.POST.get('freq', 'daily')
        visit_id = md5(name.encode('utf-8') + str(request.session.get('account')['id'])
                        + str(datetime.now().strftime("%Y%m%d%H%M%S"))).hexdigest()

        params = {'name': name, 'start': start, 'end': end,
                  'capital_base': capital_base, 'freq': freq, 'visit_id': visit_id}

        try:
            result_info = s_strategy(account_id=request.session.get('account')['id'],
                    strategy_id=None, code = request.POST.get('code', None), params=params)
            return HttpResponse(json.dumps(result_info))
        except Exception, e:
            log.error('===========Quant Template Save Error: ', e)
            return HttpResponse(json.dumps({'status': 'error', 'data': u'生成策略失败'}))
    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))


def strategy_name_validation(request):
    """
    check strategy name whether valid
    :param request:
    :return:
    """
    if request.method == 'POST':
        strategy_name = request.POST.get('strategy_name', '')
        if strategy_name != '' and len(Strategy.objects.filter(name=strategy_name)) < 1:
            print 'check valid'
            return HttpResponse(json.dumps({'status': 'ok'}))
    return HttpResponse(json.dumps({'status': 'error'}))


def code_complete(request):
    """
    /editor/code_complete
    获取补全
    :param request: POST {
        source: '',
        row: '',
        column: ''
    }
    :return: [{},]
    """
    source = request.POST.get('source')
    row = int(request.POST.get('row'))
    column = int(request.POST.get('column'))

    script = jedi.Script(source, row, column)
    completions = script.completions()
    wordlist =  map(lambda x: {'value': x.name}, completions)

    return JsonResponse(wordlist, safe=False)


def stock_complete(request):
    """
    /editor/stock_complete
    获取股票补全
    :params request: { prefix: ''}
    :return: [{},]
    """
    prefix = request.POST.get('prefix')
    limit = int(request.POST.get('limit', 100))

    if u'\u4e00' <= prefix[0] <= u'\u9fbb':
        stocks = StockSHA300.objects.filter(name__startswith=prefix)
        wordlist = map(lambda x: {'value': x.name, 'meta': x.code}, stocks)
    else:
        stocks = StockSHA300.objects.filter(code__startswith=prefix)
        wordlist = map(lambda x: {'value': x.code, 'meta': x.name}, stocks)

    values = []
    uniqueWordlist = []
    for word in wordlist:
        if word['value'] not in values and len(uniqueWordlist) < limit:
            values.append(word['value'])
            uniqueWordlist.append(word)

    return JsonResponse(uniqueWordlist, safe=False)
