#-*- coding:utf-8 -*-

from django.core.mail import send_mail
from quant_base.settings import EMAIL_HOST_USER


def _send_to_user_email(email, subject, content):
    """
    发送邮件到邮箱
    :param email:
    :param subject:
    :param content
    :return:
    """
    try:
        return send_mail(subject, content, EMAIL_HOST_USER, [email], fail_silently=False)
    except:
        return 0


def send_register_email(email, active_code):
    """
    发送激活邮件
    :param email:
    :param active_code:
    :return:
    """
    subject = u'[账号激活]欢迎使用AnyQuant'
    content = '\n'.join(["请点击以下链接以激活您的账号",
                         "http://www.anyquant.net/account/active/?code=" + active_code])
    return _send_to_user_email(email, subject, content)