#-*- coding:utf-8 -*-
__author__ = 'cheng'

import os
import pandas as pd
from quant_base.settings import STOCK_DATA_DIR

def load_custom_benchmark_data(data, symbol):
    bm_file = os.path.join(STOCK_DATA_DIR, 'bm_returns.csv')
    tr_file = os.path.join(STOCK_DATA_DIR, 'tr_curve.csv')
    bm_returns = pd.Series.from_csv(bm_file)
    tr = pd.DataFrame.from_csv(tr_file)

    bm_returns = bm_returns.tz_localize('UTC')
    tr = tr.tz_localize('UTC')

    tr_curves = {}
    for tr_dt, curve in tr.T.iterkv():
        tr_curves[tr_dt] = curve.to_dict()

    return bm_returns, tr_curves
