#-*- coding:utf-8 -*-
__author__ = 'cheng'

"""
社区功能
"""

import json, math
from datetime import datetime
import logging
import pytz

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Q

from models import Comment, CommentInfo, Category, Feedback, UserFollow
from account.models import Account

from quant_base.settings import COMMENT_PER_PAGE

from global_util.auth import login_check, captch_check

from bbs_util import post_comment, get_return_comments_list, get_recent_publish, is_user_follow

bbs_log = logging.getLogger('custom')

def bbs(request):
    """
    论坛首页，按时间降序显示最新帖子，每页默认10条,时间降序，需要分页
    参数代表过滤条件,过滤条件包括页数和话题
    :param request:
    :return: {'status': 'ok', 'data':
        {'comment': [{'title': '', 'author': '', 'date': '', 'star': ''， 're_count': '' #回帖数}],
        'category': [{'name': '', 'active': '1'}],
        'widget_info': {
            'user_post_count': '',
            'user_star_count': '',
            'user_re_count': '',
        }
        'total_pages': '',
        'active_cate_id': '',
        'page': ''}}
    """
    to_return_info = {'status': 'ok', 'data': {}}

    category_id = request.GET.get('category', '-1')
    all_category = Category.objects.all()

    target_category = Category.objects.filter(id=category_id)

    to_return_info['data']['category'] = [{'name': cate.category_name, 'id': cate.id,
        'active': 'active'  if len(target_category) > 0
        and target_category[0].category_name == cate.category_name else ''} for cate in all_category]

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

    if (current_page -1) * COMMENT_PER_PAGE > len(filtered_comments):
        current_page = 1

    comment_objects_list = filtered_comments[(current_page - 1 ) * COMMENT_PER_PAGE: current_page * COMMENT_PER_PAGE]

    comment_list = []

    for comment in comment_objects_list:
        comment_re_count = len(Comment.objects.filter(parent_id=comment.id))

        comment_star_count = len(CommentInfo.objects.filter(comment_id=comment))

        comment_list.append({'id': comment.id, 'title': comment.title, 'star': comment_star_count,
                     'author': comment.account_id.name,
                     'author_id': comment.account_id.id,
                     'content': comment.content[:20] + '...',
                     're_count': comment_re_count,
                     'date': comment.date.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')})

    to_return_info['data']['comment'] = comment_list
    to_return_info['data']['total_pages'] = int(math.ceil(len(filtered_comments) * 1.0 / COMMENT_PER_PAGE)) \
        if len(filtered_comments) > 0 else 1
    to_return_info['data']['page'] = current_page

    #计算侧边栏用户统计数据,需登录，否则不显示
    if request.session.has_key('account'):
        account_info = request.session.get('account')
        user_query = Comment.objects.filter(account_id__id=account_info['id'])
        to_return_info['data']['widget_info'] = {
            'user_post_count': len(user_query.filter(parent_id=-1)),
            'user_star_count': len(CommentInfo.objects.filter(account_id__id=account_info['id'])),
            'user_re_count': len(user_query.filter(~Q(parent_id=-1))),
        }


    #return HttpResponse(json.dumps(to_return_info))
    return render_to_response('quant_bbs/bbs_home.html', to_return_info, RequestContext(request))


def bbs_detail(request, comment_id):
    """
    显示某条详细的帖子，默认显示问题和前十条回复,时间降序，过滤条件包括页数
    即给定页数后，显示问题和对应页数的回复
    :param request:
    :param comment_id:
    :return: {'status': 'error',
        'data': {
            'comment': {'id': '', 'title': '', 'author': '', 'author_id': '',
                    'star': '', 'content': '', 'date': ''},
            're_comment': []，
            ‘widget_info’: {
                'author_post': [{'title': '', 'id': ''}]
            }}}
    """

    try:
        comment = Comment.objects.get(id=int(comment_id))

        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1

        filter_re_comment_list = Comment.objects.filter(parent_id=comment_id)\
            .order_by('date').all()
        re_comment_list = filter_re_comment_list[(page-1) * COMMENT_PER_PAGE: page * COMMENT_PER_PAGE]

        to_return_info = {'status': 'ok', 'data': {'re_comment': []}}

        comment_star_count = len(CommentInfo.objects.filter(comment_id=comment.id))
        to_return_info['data']['comment'] = {'id': comment.id, 'title': comment.title,
                                             'author': comment.account_id.name,
                                             'author_id': comment.account_id.id,
                                             'star': comment_star_count,
                                             'content': comment.content,
                                             'date': comment.date.astimezone(
                                                 pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')}

        for re_comment in re_comment_list:
            re_comment_star = len(CommentInfo.objects.filter(comment_id=re_comment.id))

            to_return_info['data']['re_comment'].append({'id': re_comment.id,
                                'title': re_comment.title, 'star': re_comment_star,
                                'author': re_comment.account_id.name,
                                'author_id': re_comment.account_id.id,
                                'content': re_comment.content,
                                'date': re_comment.date.astimezone(
                                    pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')})

        to_return_info['data']['page'] = page
        to_return_info['data']['total_pages'] = int(math.ceil(len(re_comment_list) * 1.0 / COMMENT_PER_PAGE)) \
            if len(re_comment_list)>0 else 1

        #return json for test
        #return HttpResponse(json.dumps(to_return_info))

        #计算当前帖子作者发表过的帖子,最多取三个
        author_other_comment_list = Comment.objects.filter(account_id=comment.account_id) \
            .filter(parent_id=-1).filter(~Q(id=comment.id)).order_by('-date')[:3]

        to_return_info['data']['widget_info'] = {'author_post': \
            [{'title': comment.title, 'id': comment.id} for comment in author_other_comment_list]}

        return render_to_response('quant_bbs/bbs_detail.html', to_return_info, RequestContext(request))
    except Exception, e:
        bbs_log.error("===============bbs detail error: ", e)
        return redirect('/bbs')


@login_check
def bbs_create(request):
    all_category_objects = Category.objects.all()

    all_category = [{'name': category.category_name, 'id': category.id} for category in all_category_objects]

    to_return_info = {'category': all_category}

    return render_to_response('quant_bbs/bbs_create.html', to_return_info, RequestContext(request))

@login_check
@captch_check
def bbs_submit(request):
    """
    发帖，回复帖子, POST方法 ajax方法
    :param request:
        {'account_id': '', #session中保存，不需要在post参数中发送
        'title': '' #如果是回复，不需要
        'content': '' #内容，保存html内容 #todo
        'parent_id': '' #如无则为-1
        'code': '' #验证码
        }
    :return: {‘status’: 'ok', ''}
    """
    if request.method == 'POST':
        account_id = request.session.get('account')
	print account_id

        flag = post_comment(account_id=account_id['id'], title=request.POST.get('title'),
                     content=request.POST.get('content'),
                     parent_id=int(request.POST.get('parent_id', -1)),
                     category_id=int(request.POST.get('category_id', 1)))
	print flag

        if flag:
            return HttpResponse(json.dumps({'status': 'ok'}))
        else:
            return HttpResponse(json.dumps({'status': 'error', 'data': u'发生错误'}))


@login_check
def bbs_star(request):
    """
    对某帖子(包括问题和回复)点赞，ajax方法
    :param request: {'account_id': '' #在session中，无需放到post参数中
        'comment_id': ''}
    :return:
    """
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')

        try:
            account_id = request.session.get('account').get('id')
            account = Account.objects.get(id=account_id)

            comment_info = CommentInfo.objects.filter(comment_id__id=comment_id).filter(account_id=account)

            if len(comment_info) > 0:
                return HttpResponse(json.dumps({'status': 'error', 'data': u'您已经点过赞'}))
            else:
                new_comment_info = CommentInfo()

                new_comment_info.comment_id = Comment.objects.get(id=comment_id)
                new_comment_info.account_id = account
                new_comment_info.star_date = datetime.now()

                new_comment_info.save()

                return HttpResponse(json.dumps({'status': 'ok',
                            'count': len(CommentInfo.objects.filter(comment_id=comment_id))}))
        except Exception, e:
            bbs_log.error("===========bbs star error: ", e)
            return HttpResponse(json.dumps({'status': 'error', 'data': u'ops,系统发生错误'}))


def bbs_search(request):
    """
    搜索帖子，包括标题，内容，作者, GET方法
    :param request: search: ''
    :return: {'status': 'ok', 'data': [{}]}
    """
    search_keyword = request.GET.get('search')

    if search_keyword:
        to_return_info = {'status': 'ok', 'data': {}}

        search_results = Comment.objects.filter(
            Q(title__contains=search_keyword) | Q(content__contains=search_keyword)
            | Q(account_id__name__contains=search_keyword)).all()

        comment_list = []

        for result in search_results:
            #id title star author author_id content re_count
            result_star = len(CommentInfo.objects.filter(comment_id__id=result.id))
            result_re_count = len(Comment.objects.filter(parent_id=result.id))
            comment_list.append({'id': result.id, 'title': result.title, 'star': result_star,
                                'author': result.account_id.name,
                                'author_id': result.account_id.id,
                                'content': result.content[:20],
                                're_count': result_re_count,
                                'date': result.date.astimezone(pytz.timezone('Asia/Shanghai'))
                                    .strftime('%Y-%m-%d %H:%M:%S')})

        to_return_info['data']['comment'] = comment_list

        return render_to_response('quant_bbs/bbs_home.html', to_return_info, RequestContext(request))
    return redirect('/bbs')


#侧边栏接口方法
def bbs_home_wiget_user(request):
    """
    bbs首页进来后的侧边栏，显示用户点赞数，发表文章数，评论数
    :param request: account_id
    :return:
    """
    if request.session.has_key('account'):
        #如果没有登录，
        account_info = request.session.get('account')

        comment_star_count = len(CommentInfo.objects.filter(account_id__id=account_info['id']))


def bbs_detail_wiget_recom(request):
    """
    bbs详情页面，侧边栏显示当前帖子作者发表的文章
    :param request:
    :return:
    """
    pass

#管理员操作 #TODO
def bbs_delete(request):
    """
    删除对应的帖子
    :param request:
    :return:
    """
    pass


@login_check
def feedback(request):
    """
    ajax方法，提交用户反馈
    :param request: {'account_id': '0', 'feedback_content': ''}
    :return:
    """
    if request.method == 'POST':
        account = request.session.get('account')
        account_id = account.get('id', 0)

        feedback_content = request.POST.get('feedback_content')

        if feedback_content:

            try:
                fdback = Feedback()
                fdback.account_id = Account.objects.get(id=account_id)
                fdback.content = feedback_content
                fdback.date = datetime.now()

                fdback.save()
                return HttpResponse(json.dumps({'status': 'ok', 'data': u'提交成功'}))
            except:
                return HttpResponse(json.dumps({'status': 'error', 'data': u'ops, 系统发生错误'}))

    return HttpResponse(json.dumps({'status': 'error', 'data': u'提交反馈失败'}))

@login_check
def follow_user(request):
    """
    ajax方法， POST，关注用户
    :param request: {'account_id': 1}
    :return:
    """
    if request.method == 'POST':
        login_account_id = request.session['account']['id']

        target_account_id = request.POST.get('account_id')
        try:
            to_account = Account.objects.get(id=target_account_id)
            from_account = Account.objects.get(id=login_account_id)

            user_follow = UserFollow(from_account=from_account,
                                     to_account=to_account, follow_date=datetime.now(pytz.UTC))
            user_follow.save()
            return HttpResponse(json.dumps({'status': 'ok', 'data': u'关注成功'}))
        except:
            return HttpResponse(json.dumps({'status': 'error', 'data': u'关注失败'}))

_TYPE_DICT = {'all': '动态', 'publish': '发表', 'comment': '评论', 'star': '赞'}

@login_check
def bbs_profile(request, account_id):
    """
    个人主页，显示对应发表评论点赞的帖子
    :param request: {'type':表示选择的是动态(all)、发表(publish)、评论(comment)、赞(star)中的一个 }
    :param account_id: 当前被访问的个人主页的用户id
    :return: {'status': 'ok', 'data': {
                    'user_com_count': 用户收到的评论数
                    'user_star_count': 用户收到的点赞数
                    'account_id': 当前访问用户的id
                    'account_name': 当前访问用户的name
                    'comment': [{'id': '', 'title': '', 'star': '',多个帖子的信息
                                'author': '',
                                'author_id': '',
                                'content': '',
                                're_count': '',
                                'date': ''},{},{}...]
                    'recent_publish': [{},{}] 结构与 comment相同
                    'follower': 1,
                    'following': 1,
                    'is_following': 1/0 true/false
                    }}
    """
    to_return_info = {'status': 'ok', 'data': {}}
    try:
        #防止恶意访问不存在用户
        to_return_info['data']['account_id']=account_id
        to_return_info['data']['account_name']=Account.objects.get(id=account_id).name
    except:
        return redirect('/bbs')

    #获取当前用户关注和被关注信息
    to_return_info['data']['follower'] = len(UserFollow.objects.filter(to_account__id=account_id))
    to_return_info['data']['following'] = len(UserFollow.objects.filter(from_account__id=account_id))
    #登录用户是否已关注当前访问用户
    to_return_info['data']['is_following'] = 1 if is_user_follow(request.session['account']['id'], account_id) \
        else 0

    activity_type = request.GET.get('type', 'all')
    if activity_type not in _TYPE_DICT.keys():
        activity_type = 'all'

    #排序暂时按key排序，后面如果扩展可能需要额外设置一个排序key
    to_return_info['data']['type'] = [{'type': t[0], 'active': 'active' if t[0]==activity_type else '', 'name': t[1]}
                                      for t in sorted(_TYPE_DICT.iteritems(), key = lambda x: x[0]) ]

    to_return_info['data']['active_type'] = activity_type

    my_comments = Comment.objects.filter(account_id=account_id)
    my_star_num = len(CommentInfo.objects.filter(comment_id__in=my_comments.values_list('id', flat=True)))

    my_comments = my_comments.filter(parent_id=-1)
    my_comments_num = len(Comment.objects.filter(parent_id__in=my_comments.values_list('id', flat=True)))

    to_return_info['data']['widget_info'] = {
            'user_com_count': my_comments_num,
            'user_star_count': my_star_num,
    }

    if activity_type == 'all':
        comments=CommentInfo.objects.filter(account_id__id=account_id)

        filtered_comments = Comment.objects.filter(Q(account_id__id=account_id) |
            Q(id__in=comments.values_list('comment_id', flat=True)))\
            .order_by('-date')

    elif activity_type == 'publish':
        filtered_comments = Comment.objects.filter(parent_id=-1)\
            .filter(account_id__id=account_id).order_by('-date')

    elif activity_type == "comment" :
        filtered_comments = Comment.objects.filter(~Q(parent_id=-1)). \
            filter(account_id=account_id).order_by('-date')

    elif activity_type == "star":
        comments = CommentInfo.objects.filter(account_id__id=account_id)
        filtered_comments = Comment.objects.filter(id__in=comments.values_list('comment_id', flat=True))\
            .order_by('-date')
    else:
        return redirect('/bbs')

    to_return_info['data']['comment'] = get_return_comments_list(filtered_comments[:5])

    to_return_info['data']['recent_publish'] = get_return_comments_list(get_recent_publish(account_id))

    return render_to_response('quant_bbs/bbs_profile.html', to_return_info, RequestContext(request))
