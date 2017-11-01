# -*- coding:utf-8 -*-

import pytz
import math
import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Q

from quant_bbs.models import Comment,CommentInfo,Category, UserFollow
from account.models import Account
from quant_base.settings import COMMENT_PER_PAGE, STRATEGY_PER_PAGE, USER_PER_PAGE
from quant_lab.models import Strategy, StrategyIns

from global_util.auth import admin_check
import traceback

@admin_check
def admin_home(request):
    """
    管理员首页
    tab形式显示，分别是策略管理，论坛管理，用户管理
    :param request:
    :return:
    """
    return render_to_response('quant_admin/admin_home.html', RequestContext(request))


@admin_check
def admin_strategy_show(request):
    """
    显示用户已创建的策略,按照用户来分类，按照策略的结束时间排序
    :param request:
    :return:{'status':'ok', 'data': 
            {'strategy': [{'name': '', 'id': '', 'start': '', 'end': '' , 'author_id': '', 'author_name':''}],
            'page': 1
            'total_pages': 3}}
    """
    to_return_info = {'status': 'ok', 'data': {}}

    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    if page < 0:
        page = 1

    account_all = Account.objects.all()
    strategy_all = Strategy.objects.all()

    if (page - 1) * STRATEGY_PER_PAGE > len(strategy_all):
        page = 1

    strategy = []
    for account in account_all:
        strategy_objects = Strategy.objects.filter(account_id=account).order_by('-end')
        for s in strategy_objects:
            strategy.append({'name': s.name, 'id': s.id, 'start': s.start, 'end': s.end,
                             'author_id': account.id, 'author_name': account.name})

    strategy = strategy[(page - 1) * STRATEGY_PER_PAGE: page * STRATEGY_PER_PAGE]

    total_pages = int(math.ceil(len(strategy_all) * 1.0 / STRATEGY_PER_PAGE))\
            if len(strategy_all) > 0 else 1

    to_return_info['data']['strategy'] = strategy
    to_return_info['data']['page'] = page
    to_return_info['data']['total_pages'] = total_pages

    return render_to_response('quant_admin/admin_strategy.html', to_return_info, RequestContext(request))


@admin_check
def admin_strategy_detail(request, strategy_id):
    '''
    /admin/strategy/<strategy_id>
    '''
    """
    显示具体策略
    :param request:
    :return:{'status':'','data':
            {'id': '', 'name': '', 'account_id': '',
                        'account_name': '', 'start': '', 'end': ''}}
    """
    to_return_info = {'status': '', 'data': {}}
    try:
        strategy = Strategy.objects.get(id=strategy_id)
        to_return_info['status'] = 'ok'
        to_return_info['data'] = {'name': strategy.name, 'id': strategy.id, 'start': strategy.start,
                                       'end': strategy.end, 'account_id': strategy.account_id.id,
                                       'account_name': strategy.account_id.name}
        return render_to_response('quant_admin/strategy_detail.html', to_return_info, RequestContext(request))
    except:
        # 对于查看id不存在的策略,或者id不能转化为int类型
        to_return_info['status'] = 'error'
        return render_to_response('quant_admin/strategy_detail.html', to_return_info, RequestContext(request))


@admin_check
def admin_strategy_del(request):
    """
    删除策略,删除对应的策略
    :param request:
    :return:{'status':'', 'data':''}
    """
    if request.method == 'POST':
        try:
            strategy_id = int(request.POST.get('id', 0))
            StrategyIns.objects.filter(strategy_id__id=strategy_id).delete()
            Strategy.objects.get(id=strategy_id).delete()
        except:
            return HttpResponse(json.dumps({'status': 'error', 'data': u'删除失败'}))
        else:
            return HttpResponse(json.dumps({'status': 'ok'}))
    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))


@admin_check
def admin_strategy_search(request):
    """
    根据关键字查找策略,用户名字和策略名字
    :param request:
    :return:{'status': 'ok',
        {'strategy':
        ['name': '', 'id': '', 'start': '', 'end': '', 'author_id': '', 'author_name': '']}
    """
    keyword = request.GET.get('search')
    if keyword:
        strategy_filter_result = Strategy.objects.filter(Q(account_id__name__contains=keyword)
                                                             | Q(name__contains=keyword))
        to_return_info = {'status': 'ok', 'strategy': []}
        strategy_to_return = []

        for strategy in strategy_filter_result:
            strategy_to_return.append({'name': strategy.name,
                                       'id': strategy.id,
                                       'start': strategy.start,
                                       'end': strategy.end,
                                       'author_name': strategy.account_id.name,
                                       'author_id': strategy.account_id.id})
        to_return_info['strategy'] = strategy_to_return

        return render_to_response('quant_admin/strategy.html', to_return_info, RequestContext(request))
    return redirect('/admin/strategy/')


@admin_check
def admin_bbs_show(request):
    """
    显示所有已经创建的帖子，按时间降序排列
    分类查找（策略，研究，吐槽） 页数显示
    显示帖子不包括回帖
    :param request:
    :return: {'status': 'ok', 'data':
        {'comment': [{'title': '', 'author': '', 'date': '', 'star': ''， 're_count': '' #回帖数}],
        'category': [{'name': '', 'id':'' ,'active_cate_id': '1'}],
        'total_pages': '',
        'active_cate_id': '',
        'page': ''}}
    """
    to_return_info = {'status': 'ok', 'data': {}}

    category_id = request.GET.get('category', '-1')
    all_category = Category.objects.all()

    target_category = Category.objects.filter(id=category_id)

    to_return_info['data']['category'] = [{'name': cate.category_name, 'id': cate.id, 'active': 'active'
                    if len(target_category) > 0 and target_category[0].category_name == cate.category_name else ''
                                           } for cate in all_category]

    to_return_info['data']['category'].insert(0, {'name': u'所有', 'id': -1, 'active': 'active'
                    if len(target_category) == 0 else ''})

    to_return_info['data']['active_cate_id'] = -1

    filtered_comments = Comment.objects

    if len(target_category) > 0:
        filtered_comments = filtered_comments.filter(category_id=target_category[0])
        to_return_info['data']['active_cate_id'] = target_category[0].id

    filtered_comments = filtered_comments.filter(parent_id=-1).order_by('-date').all()

    try:
        current_page = int(request.GET.get('page', 1))
        if current_page < 1:
            current_page = 1
    except ValueError:
        current_page = 1

    if (current_page - 1) * COMMENT_PER_PAGE > len(filtered_comments):
        current_page = 1

    comment_list = []
    comment_object_list = filtered_comments[(current_page-1)*COMMENT_PER_PAGE: current_page*COMMENT_PER_PAGE]

    for comment in comment_object_list:
        comment_star_count = len(CommentInfo.objects.filter(comment_id__id=comment.id))

        comment_re_count = len(Comment.objects.filter(parent_id=comment.id))

        comment_list.append({'id': comment.id,
                             'title': comment.title,
                             'author': comment.account_id.name,
                             'author_id': comment.account_id.id,
                             'content': comment.content[:10] + "...",
                             'star': comment_star_count,
                             're_count': comment_re_count,
                             'date': comment.date.astimezone(pytz.timezone('Asia/Shanghai'))
                             .strftime('%Y-%m-%d %H:%M:%S')})

    to_return_info['data']['comment'] = comment_list

    to_return_info['data']['total_pages'] = int(math.ceil(len(filtered_comments)*1.0 / COMMENT_PER_PAGE))\
         if len(filtered_comments) > 0 else 1

    to_return_info['data']['page'] = current_page

    return render_to_response('quant_admin/admin_bbs.html', to_return_info, RequestContext(request))

@admin_check
def admin_bbs_del(request):
    """
    删除特定的帖子(ajax方法的调用)
    删除回复这个的帖子（parent_id)
    删除这个帖子的点赞记录
    :param request:
    :return: {'status':'', 'data':''}
    """
    if request.method == 'POST':
        try:
            bbs_id = int(request.POST.get('id'))
            # 依次删除, 注意外键依赖
            CommentInfo.objects.filter(comment_id__id=bbs_id).delete()

            Comment.objects.get(id=bbs_id).delete()
            Comment.objects.filter(parent_id=bbs_id).delete()
        except Exception:
            return HttpResponse(json.dumps({'status': 'error', 'data': u'删除出错'}))
        else:
            return HttpResponse(json.dumps({'status': 'ok'}))

    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))


@admin_check
def admin_bbs_search(request):
    """
    提供基于bbs论坛的查找，作者的姓名，帖子的内容，帖子的标题
    :param request:
    :return:
    """
    to_return_info = {'status': 'ok', 'data': {}}
    keyword = request.GET.get('search')
    if keyword:
        search_results = Comment.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword) |
                                                Q(account_id__name__contains=keyword)).all()
        comment_list = []
        for comment in search_results:
            star = len(CommentInfo.objects.filter(comment_id__id=comment.id))
            re_count = len(Comment.objects.filter(parent_id=comment.id))
            comment_list.append({'id': comment.id,
                                 'author': comment.account_id.name,
                                 'author_id': comment.account_id.id,
                                 'content': comment.content[:10] + "...",
                                 'star': star,
                                 're_count': re_count,
                                 'date': comment.date.astimezone(pytz.timezone('Asia/Shanghai'))
                                 .strftime('%Y-%m-%d %H:%M:%S')})
        to_return_info['data']['comment'] = comment_list
        return render_to_response('quant_admin/admin_bbs.html', to_return_info, RequestContext(request))
    return redirect('admin/bbs')


@admin_check
def admin_user_show(request):
    """
    显示所有注册的用户 20行一面
    :param request:
    :return: {'status': 'ok', 'data':
        {'account': [{'account_id':'','account_name':'','account_email':'','account_post_count':''}],
        'total_pages': '',
        'page': ''}}
    """
    to_return_info = {'status': 'ok', 'data': {}}
    try:
        current_page = int(request.GET.get('page', 1))
        if current_page < 0:
            current_page = 1
    except ValueError:
        current_page = 1

    accounts_all = Account.objects.all()

    # 一页一页向上加,加到最后又回到开始
    if (current_page - 1) * USER_PER_PAGE > len(accounts_all):
        current_page = 1

    accounts_objects_list = accounts_all[(current_page-1)*USER_PER_PAGE: current_page*USER_PER_PAGE]

    accounts_list = []
    for account in accounts_objects_list:
        user_query = Comment.objects.filter(account_id__id=account.id)
        accounts_list.append({'account_id': account.id,
                              'account_name': account.name,
                              'account_email': account.email,
                              'account_post_count': len(user_query.filter(parent_id=-1)),
                              'account_star_count': len(CommentInfo.objects.filter(account_id__id=account.id)),
                              'account_re_count': len(user_query.filter(~Q(parent_id=-1)))
                              })
    to_return_info['data']['account'] = accounts_list
    to_return_info['data']['total_pages'] = int(math.ceil(len(accounts_all)*1.0/USER_PER_PAGE))\
            if len(accounts_all) > 0 else 1
    to_return_info['data']['page'] = current_page

    # return HttpResponse(to_return_info['data']['account'])
    return render_to_response('quant_admin/admin_user.html', to_return_info, RequestContext(request))


@admin_check
def admin_user_search(request):
    """
    关键字索搜用户,根据姓名
    :param request:
    return: {'status': 'ok', 'data':
        {'account': ['account_id':'','account_name':'','account_email':''],
        }}
    """
    keyword = request.GET.get('search')
    if keyword:
        to_return_info = {'status': 'ok', 'data': {}}
        name_result = Account.objects.filter(name__contains=keyword)
        if len(name_result) == 0:
            return render_to_response('quant_admin/admin_user.html', to_return_info, RequestContext(request))

        account_list = []
        for account in name_result:
            account_list.append({'account_id': account.id,
                                 'account_name': account.name,
                                 'account_email': account.email})
        to_return_info['data']['account'] = account_list
        return render_to_response('quant_admin/admin_user.html', to_return_info, RequestContext(request))
    return redirect('/admin/user')


@admin_check
def admin_user_del(request):
    """
    删除用户(ajax)方法
    删除用户，删除用户的帖子，删除用户的策略，删除用户的点赞，删除用户的评论
    :param request: id
    :return:{'status':'','data''}
    """
    if request.method == 'POST':
        try:
            account_id = int(request.POST.get('id', 0))
            account = Account.objects.get(id=account_id)

            # 删除该用户策略运行实例,
            StrategyIns.objects.filter(account_id=account).delete()

            # 删除该用户创建的策略
            Strategy.objects.filter(account_id=account).delete()

            # 删除对该用户发表过帖子的点赞记录
            comment_all = Comment.objects.filter(account_id=account)
            for comment in comment_all:
                CommentInfo.objects.filter(comment_id=comment).delete()

            # 删除该用户的点赞记录
            CommentInfo.objects.filter(account_id=account).delete()

            # 该用户发表的主帖
            parent_comment_all = Comment.objects.filter(account_id=account, parent_id=-1)

            # 删除回复该用户发表的主贴的回帖
            for parent_comment in parent_comment_all:
                Comment.objects.filter(parent_id=parent_comment.id).delete()

            # 删除用户发表(包括主帖和回帖)的帖子
            Comment.objects.filter(account_id=account).delete()

            #删除对用户的关注follow
            #删除关注者为account的记录
            UserFollow.objects.filter(to_account=account).delete()
            #删除被关注者为account的记录
            UserFollow.objects.filter(from_account=account).delete()

            # 删除相应的用户
            account.delete()

        except:
            traceback.print_exc()
            return HttpResponse(json.dumps({'status': 'error', 'data': u'删除失败'}))
        else:
            return HttpResponse(json.dumps({'status': 'ok'}))
    return HttpResponse(json.dumps({'status': 'error', 'data': u'请求方法错误'}))
