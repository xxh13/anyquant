#-*- coding:utf-8 -*-
"""
Django settings for quant_base project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1phiwz9513p2m6rxhs9!(twhje3l=9t$31q29twi1z*5^=m3kb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quant_lab',
    'account',
    'quant_bbs',
    'anyquant',
    'social',
    'quant_admin',
    'quant_data',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'quant_base.urls'

WSGI_APPLICATION = 'quant_base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quant_base',
        'HOST':  'localhost', #'121.41.106.89'
        'PORT': 3306,
        'USER': 'quant',
        'PASSWORD':  'quant', #'Sydar10',
    }
}

#log config
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        }
    }
}
"""
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR, 'static').replace('\\', '/')

#STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
)


#TEMPLATES = (
#    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#    # Always use forward slashes, even on Windows.
#    # Don't forget to use absolute paths, not relative paths.
#    os.path.join(BASE_DIR, "templates").replace("\\", "/"),
#)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],           # templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
	#'TEMPLATE_DEBUG': False,
	#'TEMPLATE_CONTEXT_PROCESSORS': [
	#  "django.core.context_processors.request",
	#  "django.contrib.auth.context_processors.auth",
	#]
    },
]

#TEMPLATE_CONTEXT_PROCESSORS = (
#    "django.core.context_processors.request",
#    "django.contrib.auth.context_processors.auth",
#)

DEFAULT_INDEX_TABLESPACE = ""

STOCK_DATA_DIR = os.path.join(BASE_DIR, 'data').replace('\\', '/')

#存放策略文件
CODE_DIR = os.path.join(BASE_DIR, 'code').replace('\\', '/')

#存放策略运行文件
CODE_INS_DIR = os.path.join(BASE_DIR, 'code_ins').replace('\\', '/')

#存放分享代码文件
SHARE_CODE_DIR = os.path.join(BASE_DIR, 'share_code').replace('\\', '/')

COMMENT_PER_PAGE = 10
STRATEGY_PER_PAGE = 10
USER_PER_PAGE = 10
STOCK_PER_PAGE = 20

#EMAIl 配置
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.163.com'
EMAIL_HOST_USER='15850781776@163.com'
EMAIL_HOST_PASSWORD='xxh82814680'
EMAIL_USE_TLS=True

#管理员配置
ADMIN_EMAILS = []
