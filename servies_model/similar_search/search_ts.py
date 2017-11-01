# -*- coding: utf-8 -*-
#==============================================================================
#寻找相似序列程序
#==============================================================================
import numpy as np
import pandas as pd
import datetime
import os
import sqlalchemy as sa
from matplotlib import pyplot as plt

class find_similar(object):
    def __init__(self,code,date,feature_name,step):
        '''
        code:股票代码
        date:需要搜索日期
        feature_name:首要相似属性
        step:相似搜索长度
        '''
        path_df=os.path.realpath('ts_{0}_{1}.pkl'.format(step,feature_name))
        path_df_raw=os.path.realpath('ts_raw_{0}_{1}.pkl'.format(step,feature_name))
        df=pd.read_pickle(path_df)
        df_raw=pd.read_pickle(path_df_raw)
        try:
            label=df[(df['code']==code) & (df['trade_date']==date)]['label'].values[0]
            ts_close=df[(df['code']==code) & (df['trade_date']==date)]['time_series_close'].values[0]
            ts_open=df[(df['code']==code) & (df['trade_date']==date)]['time_series_open'].values[0]
            ts_high=df[(df['code']==code) & (df['trade_date']==date)]['time_series_high'].values[0]
            ts_low=df[(df['code']==code) & (df['trade_date']==date)]['time_series_low'].values[0]
            ts_vol=df[(df['code']==code) & (df['trade_date']==date)]['time_series_volume'].values[0]
            self.erro=False
        except:
                self.erro=True
                return
        self.df=df[df['label']==label]
        self.df_raw=df_raw
        self.ts={'time_series_close':ts_close,'time_series_high':ts_high,'time_series_low':ts_low,'time_series_open':ts_open,'time_series_volume':ts_vol}

    @staticmethod
    def cos_dis(x,y):
        return np.dot(x,y)

    def count_distance(self):
        cos_dis_dict={'code':[],'trade_date':[],'time_series_close_score':[],'time_series_open_score':[],'time_series_high_score':[],'time_series_low_score':[],'time_series_volume_score':[]}
        for i in range(len(self.df)):
            for col in self.df.columns[1:-2]:
                y=self.df.iloc[i][col]
                cos_dis_dict[col+'_score'].append(self.cos_dis(self.ts[col],y))
            cos_dis_dict['code'].append(self.df.iloc[i]['code'])
            cos_dis_dict['trade_date'].append(self.df.iloc[i]['trade_date'])
        self.df_cos_dis=pd.DataFrame(cos_dis_dict)

    def summary(self,close_weight=0.6,open_weight=0.1,high_weight=0.1,low_weight=0.1,volume_weight=0.1):
        self.df_cos_dis['sum']=self.df_cos_dis['time_series_close_score']*close_weight+self.df_cos_dis['time_series_open_score']*open_weight+self.df_cos_dis['time_series_high_score']*high_weight+self.df_cos_dis['time_series_low_score']*low_weight+self.df_cos_dis['time_series_volume_score']*volume_weight
        self.df_cos_dis.sort_values(by='sum',ascending=False,inplace=True)
        self.result=self.df_cos_dis.iloc[:5]

    def statis(self,con):
        con=con.connect()
        lst=[]
        for i in range(len(self.result))[1::]:
            code=self.result.iloc[i]['code']
            trade_date=self.result.iloc[i]['trade_date']
            sql='''select p_change from quant_base.stock_data where code='{0}' and trade_date >={1} order by trade_date DESC limit 1'''.format(code,trade_date)
            lst.append(pd.read_sql(sql=sql,con=con)['p_change'].values[0])
        self.predict=lst
        con.close()

    def plot(self,plot_num=9):
        self.df_cos_dis.sort_values(by='time_series_close_score',ascending=False,inplace=True)
        df_plot=self.df_cos_dis.head(plot_num)
        fig,axes=plt.subplots(3,3)
        for i,axe in enumerate(axes.reshape(-1)):
            temp=df_plot.iloc[i]
            plot_data=self.df_raw[(self.df_raw['code']==temp['code']) & (self.df_raw['trade_date']==temp['trade_date'])]['time_series_close'].values[0]
            axe.plot(plot_data)

if __name__=='__main__':
    con=sa.create_engine('mysql://quant:quant@120.27.199.164/quant_base').connect()
    code='002044'
    date=datetime.date(2017,10,25)
    test_find_similar=find_similar(code,date,'close',5)
    print(test_find_similar.erro)
    #test_find_similar.count_distance()
    #test_find_similar.summary()
    #test_find_similar.statis(con)
    #con.close()
