# -*- coding: utf-8 -*-
#==============================================================================
#main
#==============================================================================
import numpy as np
import pandas as pd
import sqlalchemy as sa
import search_ts
import datetime

def get_con():
    con=sa.create_engine('mysql://quant:quant@120.27.199.164/quant_base')
    return con

def main(code,date,feature_name,close_weight=0.6,open_weight=0.1,high_weight=0.1,low_weight=0.1,volume_weight=0.1,step=5):
    usr=search_ts.find_similar(code,date,'close',step)
    if not usr.erro:
        usr.count_distance()
        usr.summary()
        usr.statis(get_con())
    else:
        return 'no data'
    return [usr.result,usr.predict]

if __name__=='__main__':
    code='002044'
    date=datetime.date(2017,10,1)
    feature_name='close'
    result=main(code,date,feature_name)
