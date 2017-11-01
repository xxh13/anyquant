#-*- coding:utf-8
__author__ = 'cheng'

from datetime import datetime
import pytz

from account.models import Account
from quant_base.settings import COMMENT_PER_PAGE
from models import Comment, CommentInfo, Category, UserFollow


def post_comment(account_id, title, content, parent_id=-1, category_id=1):
    """
    发帖
    :param account_id:
    :param title:
    :param content:
    :param parent_id:
    :return:
    """
    try:
        account = Account.objects.get(id=account_id)
        category = Category.objects.get(id=category_id)

        comment = Comment(account_id=account, category_id=category, title=title, content=content,
                      parent_id=parent_id, date=datetime.now())

        comment.save()
        return comment.id, True
    except Exception, e:
        print e
        return None, False


def get_current_page(request, filtered_comments):
    """
    获取当前页号
    :param request:
    :param filtered_comments:
    :return:current_page
    """

    try:
        current_page = int(request.GET.get('page', 1))
        if current_page < 1:
            current_page = 1
    except ValueError:
        current_page = 1

    if (current_page -1) * COMMENT_PER_PAGE > len(filtered_comments):
        current_page = 1
    return current_page


def get_return_comments_list(comment_objects_list):
    """
    获取填入数据后将要返回的帖子列表
    :param comment_objects_list:
    :param comments_list:
    :return:comments_list
    """
    comments_list = []
    for comment in comment_objects_list:
        comment_re_count = len(Comment.objects.filter(parent_id=comment.id))
        comment_star_count = len(CommentInfo.objects.filter(comment_id=comment))
        comments_list.append({'id': comment.id, 'title': comment.title, 'star': comment_star_count,
                 'author': comment.account_id.name,
                 'author_id': comment.account_id.id,
                 'content': comment.content[:20] + '...',
                 're_count': comment_re_count,
                 'date': comment.date.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')})
    return comments_list


def get_recent_publish(account_id):
    """
    获取最近发表的3条帖子
    :param account_id:
    :return:my_recent_pub_top3
    """
    my_recent_pub = Comment.objects.filter(parent_id=-1).filter(account_id=account_id).order_by('-date').all()
    my_recent_pub_top3 = my_recent_pub[:3]
    return  my_recent_pub_top3


def is_user_follow(from_account_id, to_account_id):
    """
    检查是否是关注关系
    :param from_account_id: 关注者id
    :param to_account_id: 被关注者id
    :return:
    """
    if len(UserFollow.objects.filter(from_account__id=from_account_id)
                   .filter(to_account__id=to_account_id)) > 0:
        return True
    return False
