#-*- coding:utf-8 -*-

from django.db import models


class Share(models.Model):
    """
    保存分享链接和内容
    """
    id = models.AutoField(primary_key=True)

    account_id = models.ForeignKey('account.Account', db_column='account_id')
    strategy_id = models.ForeignKey('quant_lab.Strategy', db_column='strategy_id')

    url = models.CharField(max_length=100, db_column='share_link')
    date = models.DateTimeField()

    share_code_path = models.CharField(max_length=200)
    result_params = models.TextField()
    svg_content = models.TextField()

    class Meta:
        db_table = 'social_share'
