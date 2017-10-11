# -*- coding:utf-8 -*-

import os
from quant_base.settings import SHARE_CODE_DIR


def store_share_code(account_id, strategy_id, strategy_code_path, share_code):
    """
    保存当前分享的代码
    :param account_id:
    :param strategy_id:
    :param share_code:
    :return: share_code_path
    """
    share_code_dir = os.path.join(SHARE_CODE_DIR, str(account_id),
                                  str(strategy_id))

    if os.path.isdir(share_code_dir) is not True:
        os.makedirs(share_code_dir)

    share_code_path = os.path.join(share_code_dir, str(share_code) + ".py")
    try:
        with open(strategy_code_path, 'rb') as code_file:
            code = ''.join(code_file.readlines())

        with open(share_code_path, 'wb') as share_code_file:
            share_code_file.write(code)

        return share_code_path
    except:
        return None


def get_share_code(share_code_path):
    """
    读取分享的代码
    :param share_code_path:
    :return:
    """
    try:
        with open(share_code_path, 'rb') as code_file:
            code = ''.join(code_file.readlines())

        return code
    except:
        return ''


def concat_comment(origin_content, extra_params):
    """
    生成帖子内容，根据不同参数不一样
    code: 代表代码 渲染输出
    result_params: 参数 dict，转换成table dom元素
    svg_content: svg图，直接输出
    :param origin_content:
    :param kwargs:
    :return:
    """
    content_list = [origin_content]
    if extra_params.has_key('code'):
        #防止unicode解码错误，下同
        try:
            code = extra_params.get('code').decode('utf-8')
        except:
            code = extra_params.get('code')
        #设置代码高亮格式
        content_list.append("<pre><code class='python'>" + code + "</code></pre>")

    if extra_params.has_key('result_parmas'):
        try:
            result_params = extra_params.get('result_params').decode('utf-8')
        except:
            result_params = extra_params.get('result_params')
        content_list.append(result_params)

    if extra_params.has_key('svg_content'):
        try:
            svg_content = extra_params.get('svg_content').decode('utf-8')
        except:
            svg_content = extra_params.get('svg_content')
        content_list.append(svg_content)

    return '<br/>'.join(content_list)
