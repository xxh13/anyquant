#-*- coding:utf-8 -*-
__author__ = 'cheng'


import os
from datetime import datetime
import pytz
import time

from models import Strategy, StrategyIns, StrategyCate, StrategyCateData
from account.models import Account

from quant_base.settings import CODE_DIR, CODE_INS_DIR


def save_strategy(account_id, strategy_id=None, code=None, params=None):
    """
    保存策略，包括策略代码文件和策略参数
    1, 如果strategy_id 为None，说明是新建策略，
        code为None，默认代码，否则为模板代码，保存代码
    2，如果strategy_id 不为None，说明为更新策略
    :param account_id:
    :param strategy_id
    :param code
    :param params: {'start': '', 'end': '', 'capital_base': '', 'freq': ''}
    :return:
    """
    if strategy_id:
        #更新策略信息
        try:
            strategy = Strategy.objects.get(id=int(strategy_id))
        except Exception, e:
            return {'status': 'error', 'data': 'no such strategy'}
    else:
        strategy = Strategy()

    try:
        #保存参数, 注意一些必须参数
        strategy.name = params.get('name', strategy.name)
        strategy.start = datetime.strptime(params.get("start", strategy.start), "%Y-%m-%d")
        strategy.end = datetime.strptime(params.get("end", strategy.end), "%Y-%m-%d")
        strategy.capital_base = params.get('capital_base', strategy.capital_base)
        strategy.freq = 'daily' if params.get('freq', u'每天') == u'每天' else 'minute'
        strategy.account_id = Account.objects.get(id=account_id)
        strategy.visit_id = params.get('visit_id', strategy.visit_id)

        strategy.save()

        if not strategy_id:
            #新建策略，需要再保存代码后设置file_path，再保存
            strategy_id = strategy.id
            strategy.file_path = save_code_file(account_id, strategy_id, code)
            strategy.save()

        return {'status': 'ok', 'strategy_visit_id': strategy.visit_id}
    except Exception, e:
        return {'status': 'error', 'data': 'save strategy failed'}


def save_strategy_ins(account_id, strategy_id, ins_file_path, result, info):
    strategy_ins = StrategyIns()
    strategy_ins.account_id = Account.objects.get(id=account_id)
    strategy_ins.strategy_id = Strategy.objects.get(id=strategy_id)
    strategy_ins.file_path = ins_file_path
    strategy_ins.result = result
    strategy_ins.info = info
    strategy_ins.date = datetime.now(tz=pytz.UTC)

    try:
        strategy_ins.save()
    except:
        return

def save_code_file(account_id, strategy_id, code=None):
    """
    保存当前最新的策略代码文件
    在每次运行策略或保存时触发
    注意：区别于保存运行策略时的策略实例代码
    保存规则为 account_id strategy_id
    :param code:
    :return:
    """
    if code is None:
        with open(CODE_DIR + '/code_init.py', 'rb') as code_init_file:
            code = ''.join(code_init_file.readlines()).decode('utf8')

    code_target_dir = os.path.join(CODE_DIR, str(account_id))

    if not os.path.exists(code_target_dir):
        os.makedirs(code_target_dir)

    with open(os.path.join(code_target_dir, str(strategy_id) + '.py'), 'wb') as code_write_file:
        code_write_file.write(code.encode('utf8'))

    return os.path.join(code_target_dir, str(strategy_id) + '.py')


def save_code_ins_file(account_id, strategy_id, code):
    """
    保存每次运行时策略实例代码
    在每次运行策略时触发 CODE_INS_DIR/account_id/strategy_id-datetime.py
    :param code:
    :return:
    """
    code_ins_target_dir = os.path.join(CODE_INS_DIR, str(account_id))

    if not os.path.exists(code_ins_target_dir):
        os.makedirs(code_ins_target_dir)

    target_code_ins_file = str(strategy_id) + '-' \
                           + datetime.now().strftime('%Y%m%d%H%M%S%s') + '.py'

    with open(os.path.join(code_ins_target_dir, target_code_ins_file), 'wb') as ins_file:
        ins_file.write(code.encode('utf8'))

    return os.path.join(code_ins_target_dir, target_code_ins_file)


def get_strategy_info(strategy_visit_id, account_id):
    """
    获取给定id的策略文件信息
    :param strategy_id: 策略文件id
    :param account_id: 账号id
    :return:
    """
    strategy = Strategy.objects.get(visit_id=strategy_visit_id)

    if strategy and strategy.account_id_id == account_id:
        with open(strategy.file_path, 'rb') as code_file:
            code = ''.join(code_file.readlines())

        return {'id': strategy.id,
                'name': strategy.name,
                'code': code, 'start': strategy.start.astimezone(
                    pytz.timezone("Asia/Shanghai")).strftime('%Y-%m-%d'),
                'end': strategy.end.astimezone(pytz.timezone("Asia/Shanghai")).strftime('%Y-%m-%d'),
                'capital_base': strategy.capital_base,
                'freq': u'每天' if strategy.freq == 'daily' else u'每分钟'}
    return {'id': 'demo',
            'name': u'演示策略',
            'code': '', 'start': datetime.now().astimezone(
                    pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d"),
            'end': datetime.now().astimezone(
                    pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d"),
            'capital_base': 200000,
            'freq': u'每天'}


def get_filter_strategy_list(account_id, cate=None):
    """
    根据过滤条件获取对应的策略列表
    :param account_id:
    :param cate: 分类的visit_id
    :return:
    """
    all_strategy_objects = Strategy.objects.filter(account_id__id=account_id)
    if cate is not None:
        #获取分类过滤数据
        if cate == 'default':
            #default 获取非分类数据表中其他数据
            filtered_ids = [s.strategy_id.id for s in StrategyCateData.objects.filter(account_id__id=account_id)]
            all_strategy_objects = all_strategy_objects.exclude(id__in=filtered_ids)
        else:
            #根据cate visit_id 过滤
            all_strategy_objects = [s.strategy_id for s in
                                    StrategyCateData.objects.filter(strategy_cate_id__visit_code=cate)]
            return sorted(all_strategy_objects, key=lambda x: x.end, reverse=True)

    return all_strategy_objects.order_by('-end')


def get_current_category(account_id, cate_visit_id):
    if cate_visit_id is None:
        return {'name': u'所有', 'visit_id': '', 'id': ''}
    elif cate_visit_id == 'default':
        return {'name': u'默认', 'visit_id': 'default', 'id': '-1'}
    else:
        try:
            current_cate = StrategyCate.objects.get(visit_code=cate_visit_id)
            return {'name': current_cate.name, 'visit_id': current_cate.visit_code, 'id': current_cate.id}
        except:
            return {'name': u'所有', 'visit_id': '', 'id': ''}
    return {'name': u'所有', 'visit_id': '', 'id': ''}


def get_category_info_by_strategy(strategy_id):
    try:
        straegy_cate_data = StrategyCateData.objects.get(strategy_id__id=strategy_id)
        return {'name': straegy_cate_data.strategy_cate_id.name, 'id': straegy_cate_data.strategy_cate_id.id}
    except:
        return {'name': u'默认', 'id': '-1'}

def check_category_valid(cate_name, account_id):
    if cate_name == u'默认' or len(StrategyCate.objects.filter(account_id__id=account_id, name=cate_name)) > 0:
        return False
    return True


def forme_date_ts(d):
    new_date = datetime(d.year, d.month, d.day)

    return time.mktime(new_date.timetuple()) * 1000