# -*- coding: utf-8 -*-
#==============================================================================
#高阶属性的计算
#==============================================================================
import pandas as pd
import sqlalchemy
import numpy as np
import sklearn
import sqlalchemy.orm
import datetime
import tushare as ts

class Config(object):
    con=sqlalchemy.create_engine('mysql://quant:quant@120.27.199.164/quant_base')
    trade_date=ts.trade_cal()
    trade_date=trade_date[trade_date.isOpen==1].calendarDate.tolist()[-250:]

metadata=sqlalchemy.MetaData()
table_stock_data=sqlalchemy.Table('stock_data',metadata,autoload_with=Config.con,schema=None)
class class_stock_data(object):
    def __init__(self,id,code,open,close,high,low,trade_date,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover):
        self.id=id
        self.code=code
        self.open=open
        self.close=close
        self.high=high
        self.low=low
        self.trade_date=trade_date
        self.volume=volume
        self.price_change=price_change
        self.p_change=p_change
        self.ma5=ma5
        self.ma10=ma10
        self.ma20=ma20
        self.v_ma5=v_ma5
        self.v_ma10=v_ma10
        self.v_ma20=v_ma20
        self.turnover=turnover

    def __repr__(self):
        return "{},{},{}".format(self.id,self.code,self.open)

sqlalchemy.orm.mapper(class_stock_data,table_stock_data)
DBsession=sqlalchemy.orm.sessionmaker(bind=Config.con)

class Stock_Market_Temperature(object):
    def __init__(self,date):
        '''
        :param date:datetime.date
        '''
        if str(date) not in Config.trade_date:
            self.erro=True
        else:
            self.erro=False
        sess=DBsession()
        self.data=pd.DataFrame(sess.query(table_stock_data).filter(class_stock_data.trade_date==date).all())
        sess.close()

    def feature(self,price_rise_beyond=0.05,price_fall_unfinish=0.01,turnover_beyond=5,turnover_unfinish=1):
        self.rise_stop_num=((self.data['close']-self.data['open'])/self.data['open']>0.0999).sum()
        self.fall_stop_num=((self.data['open']-self.data['close'])/self.data['open']>0.0999).sum()
        self.price_rice_beyond_num=((self.data['high']-self.data['low'])/self.data['low']>price_rise_beyond).sum()
        self.price_fall_unfinish_num=((self.data['high']-self.data['low'])/self.data['low']<price_fall_unfinish).sum()
        self.turnover_beyond_num=(self.data['turnover']>turnover_beyond).sum()
        self.turnover_unfinish_num=(self.data['turnover']<turnover_unfinish).sum()

def temperature(date):
    '''
    :param date:datetime.date
    :return :(list,[rise_stop_num,fall_stop_num,price_rice_beyond_num,
            price_fall_unfinish_num,turnover_beyond_num,turnover_unfinish_num])
    '''
    instance=Stock_Market_Temperature(date)
    if instance.erro:
        return False,'no data'
    else:
        instance.feature()
        return True,[instance.rise_stop_num,instance.fall_stop_num,
                    instance.price_rice_beyond_num,instance.price_fall_unfinish_num,
                    instance.turnover_beyond_num,instance.turnover_unfinish_num]




if __name__=='__main__':
    day_list=ts.trade_cal()[-350:-55]['calendarDate']
    dic={'rstop':[],'fstop':[],'rbeyond':[],'funfinish':[],'tbeyond':[],'tunfinish':[]}
    for day in day_list:
        ok,lst=temperature(day)
        if ok:
            print day
            dic['rstop'].append(lst[0])
            dic['fstop'].append(lst[1])
            dic['rbeyond'].append(lst[2])
            dic['funfinish'].append(lst[3])
            dic['tunfinish'].append(lst[4])
            dic['tunfinish'].append(lst[5])
