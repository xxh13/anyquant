#-*- coding:utf-8 -*-
__author__ = 'cheng'

from django.db import models


class Category(models.Model):
    """
    话题分类表，每个帖子会属于一个话题，话题预设
    策略，吐槽，研究。。。
    """
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    last_added = models.DateTimeField()

    class Meta:
        db_table = 'user_topic_category'


class Comment(models.Model):
    """
    帖子主表，外键是account
    每个帖子会有一个parent id，-1为发的帖，否则为回帖
    """
    id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey('account.Account', db_column='account_id')
    category_id = models.ForeignKey('Category', db_column='category_id', default=-1)

    parent_id = models.IntegerField()

    date = models.DateTimeField()

    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        db_table = 'user_comment'


class CommentInfo(models.Model):
    id = models.AutoField(primary_key=True)

    comment_id = models.ForeignKey('Comment', db_column='comment_id')

    account_id = models.ForeignKey('account.Account', db_column='account_id', default=-1)

    star_date = models.DateTimeField()

    class Meta:
        db_table = 'user_comment_star'


class UserFollow(models.Model):
    """
    用户之间互相关注表
    """
    id = models.AutoField(primary_key=True)

    from_account = models.ForeignKey('account.Account', db_column='from_account', related_name='user_follow_from')
    to_account = models.ForeignKey('account.Account', db_column='to_account', related_name='user_follow_to')

    follow_date = models.DateTimeField()

    class Meta:
        db_table = 'user_follow'


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)

    account_id = models.ForeignKey('account.Account', db_column='account_id')

    content = models.TextField(max_length=1024)

    date = models.DateTimeField()

    class Meta:
        db_table = 'user_feedback'
