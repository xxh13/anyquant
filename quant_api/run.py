# -*-coding: utf-8 -*-

# 测试运行服务器
from api import app
from wsgiref import simple_server

httpd = simple_server.make_server('', 8000, app)
httpd.serve_forever()