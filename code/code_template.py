#-*- coding:utf-8 -*-
import numpy as np

from zipline.api import order

# 第一步：设置基本参数
start = '2014-01-01'
end   = '2015-01-01'
capital_base = 1000000
refresh_rate = 5
benchmark = 'HS300'
freq = 'd'

# 第二步：选择主题，设置股票池
universe = []

def initialize(context):
    # 第三步：调整股票权重，权重列表序号与股票池列表序号对应
    context.weight = []
    context.weightmap = dict(zip(universe, context.weight))
    context.valid_secpos = dict(zip(universe, [0] * len(universe)))

def handle_data(context, data):
    # 本策略将使用context的以下属性：
    # context.portfolio.cash 表示根据前收计算的当前持有证券市场价值与现金之和。
    # data[<code>]['adj_pirce'] 表示股票的参考价，一般使用的是上一日收盘价。
    # account.valid_secpos字典，键为证券代码，值为虚拟账户中当前所持有该股票的数量。

    # 本策略使用context以下属性
    #

    c = context.capital_base

    # 计算调仓数量
    change = {}
    for stock in universe:
        w = context.weightmap.get(stock, 0)
        p = data[stock]['adj_price']
        if not np.isnan(p):
            change[stock] = int(c * w / p) - context.valid_secpos.get(stock, 0)
            context.valid_secpos[stock] = change[stock]

    # 按先卖后买的顺序发出指令
    for stock in sorted(change, key=change.get):
        order(stock, change[stock])
