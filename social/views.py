#-*- coding:utf-8 -*-

import os
import json
from datetime import datetime
from hashlib import md5
import logging

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from models import Share
from account.models import Account
from quant_lab.models import Strategy

from social_util import concat_comment, store_share_code, get_share_code
from quant_bbs.bbs_util import post_comment

from quant_base.settings import SHARE_CODE_DIR

social_log = logging.getLogger('custom')

def share(request):
    """
    点击分享，分享包括代码，当前结果(指数，图表), ajax方法，成功后返回生成的唯一url
    :param request:
        strategy_id   策略id
        svg_content   svg dom元素 <svg>...</svg>
        result_params  table dom元素 <table>...</table>
        title   分享帖子的标题
        comment_content   分享帖子的content
    :return:
    """
    if request.method == 'POST':
        account_info = request.session.get('account')
        account = Account.objects.get(id=account_info['id'])

        strategy_id = request.POST.get("strategy_id")
        strategy = Strategy.objects.get(id=strategy_id)

        #生成唯一url
        # /share/<identifier>
        # identifier由account id strategy id time hash 成
        date = datetime.now()

        share_code = md5('_'.join([str(account_info['id']),
                                   strategy_id, date.strftime("%Y%m%d%H%M%S")])).hexdigest()
        result_params = request.POST.get('result_params')
        svg_content = request.POST.get('svg_content')

        #保存分享时代码
        share_code_path = store_share_code(account_info['id'], strategy_id,
                                    strategy.file_path, share_code)

        if share_code_path is None:
            return HttpResponse(json.dumps({'status': 'error', 'data': u'分享失败'}))

        share = Share(account_id=account, strategy_id=strategy, url=share_code,
                      date=date, share_code_path=share_code_path,
                      result_params=result_params, svg_content=svg_content)

        try:
            share.save()

            #分享链接成功后调接口发帖
            title = request.POST.get('title', u'策略分享')
            comment_content = request.POST.get('comment_content', '')

            content = concat_comment(comment_content,
                                            {'code': get_share_code(share_code_path),
                                            'result_params': result_params,
                                            'svg_content': svg_content})

            comment_id, flag = post_comment(account_id=account_info['id'],
                                    title=title,
                                    content=content)
            if not flag:
                return HttpResponse(json.dumps({'status': 'error', 'data': '分享链接失败'}))
            return HttpResponse(json.dumps({'status': 'ok', #TODO
                                'data': u'分享成功，快去社区看看吧'}))
        except Exception, e:
            social_log.error("==========Social Error", e)
            return HttpResponse(json.dumps({'status': 'error', 'data': u'生成分享链接失败'}))

    else:
        return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))


def share_visit(request, share_code):
    """
    访问分享的页面, 读取保存的代码，运行结果并返回
    :param request: {'code': #分享的唯一标识符}
    :return: {'status': 'ok', 'data': {'code': '', 'result_params': '', 'svg_content': ''}}
    """
    share_objs = Share.objects.filter(url=share_code)
    to_return_info = {'status': 'ok',
                      'data': {'title': '',
                               'author': '',
                               'code': '',
                               'result_params': '',
                               'svg_content': ''}}
    if len(share_objs) > 0:
        share_obj = share_objs[0]

        to_return_info['data']['title'] = share_obj.strategy_id.name
        to_return_info['data']['author'] = share_obj.account_id.name
        #读取分享的代码
        to_return_info['data']['code'] = get_share_code(share_obj.share_code_path)
        to_return_info['data']['result_params'] = share_obj.result_params     #result_params table dom元素
        to_return_info['data']['svg_content'] = share_obj.svg_content     #svg dom元素

        return render_to_response('social/share.html', to_return_info, RequestContext(request))
    else:
        return render_to_response('social/share.html', to_return_info, RequestContext(request))