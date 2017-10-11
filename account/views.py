#-*- coding:utf-8 -*-
__author__ = 'cheng'

from hashlib import md5
import random
from DjangoCaptcha import Captcha

from models import Account
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from django.db.models import Q

from account_util import send_register_email
from global_util.auth import captch_check, captch_http_check


def login(request):
    """
    这里区分GET方法和POST方法，
    GET方法用于访问 /login 返回页面
    POST方法用于用户登录提交信息
    用户登录，校验正确后在request.session 中保存用户信息，如下
    request.session['account] = {'id': <account_id>,
    'email': <account_email>, 'name': <account_name>}
    这样在后面的操作中就可以通过request.session来获取用户信息了
    最后跳转到首页，这里默认先跳转到 /labs
    如果不正确，需要返回错误信息，比如用户名或密码不正确等。
    :param request:
    :return:
    """

    if request.method == 'POST':
        #name email 均唯一
        try:
            account = Account.objects.get(name=request.POST['username'])

            if not account.is_active:
                return render_to_response('account/login.html', {'error', u'该用户尚未激活，请激活'})
            if account.password != md5(request.POST['password']).hexdigest():
                return render_to_response('account/login.html', {'error': u'用户名或密码不对'})
            else:
                request.session['account'] = \
                    {'id': account.id, 'email': account.email, 'name': account.name}
                return HttpResponseRedirect('/labs/')
        except Exception, e:
            return render_to_response('account/login.html', {'error': u'不存在该用户名'})
    #GET 方法，返回对应的登录页面
    if request.method == 'GET':
        return render_to_response('account/login.html')


def logout(request):
    """
    用户登出，直接清除session并跳转到首页
    :param request:
    :return:
    """
    del request.session['account']
    return HttpResponseRedirect('/labs/')

def register(request):
    """
    用户注册页面
    需要用户填写 email，name，password
    POST请求后插入到数据库中，需要做校验
    成功后跳转到登录首页
    :param request:
    :return:
    """
    if request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not captch_http_check(request.POST.get('code', ''), request):
            return render_to_response('account/register.html',
                                      {'error': u'验证码输入错误', 'email': email,
                                       'name': username, 'password': password})
        # email和name唯一,所以进行校验，如果email已经被注册，需要再次换一个email
        result = Account.objects.filter(Q(email=email) | Q(name=username))
        #生成激活码
        code = md5(username.encode('utf-8') + str(password)).hexdigest()
        if len(result) > 0:
            error = u'邮箱或用户名已经被注册，请换一个'
            return render_to_response('account/register.html',
                                      {'error': error, 'email': email,
                                       'name': username, 'password': password})

        account = Account(email=email, name=username, password=md5(password).hexdigest(),
                          is_active=False, active_code=code)
        account.save()

        #发送邮件
        return_code = send_register_email(email, code)
        if return_code != 0:
            return render_to_response('account/register.html', {'done': 1})
        else:
            return render_to_response('account/register.html', {'error': u'发送激活邮件失败', 'email': email,
                                                                'name': username, 'password': password})

    return render_to_response('account/register.html')


def account_active(request):
    """
    激活邮件访问链接
    :param request:
    :return:
    """
    active_code = request.GET.get('code')

    if active_code:
        active_account_list = Account.objects.filter(active_code=active_code).filter(is_active=0)

        if len(active_account_list) > 0:
            active_account = active_account_list[0]

            active_account.is_active = 1

            try:
                active_account.save()
                return render_to_response('account/active.html',
                                          {'status': 'ok', 'data': u'激活成功, 可以登录'})
            except:
                return render_to_response('account/active.html',
                                          {'status': 'error', 'data': u'激活失败，请重试，如果还不行，请联系我们'})

    return render_to_response('account/active.html', {'status': 'error', 'data': u'激活码不存在或已激活'})


###used for captcha

def code(request):
    nums = [2, 3, 4, 5, 6, 7, 8, 9]

    ca = Captcha(request)
    ca.words = [''.join([str(random.sample(nums, 1)[0]) for i in xrange(0, 4)])]
    ca.type = 'word'

    return ca.display()