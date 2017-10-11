#-*- coding:utf-8 -*-
__author__ = 'cheng'

from settings import *

TEMPLATE_DEBUG = False
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quant_base',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'quant',
        'PASSWORD': 'Sydar10',
    }
}

ALLOWED_HOSTS = '*'