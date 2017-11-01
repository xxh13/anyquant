# -*- coding: utf-8 -*-
#==============================================================================
#寻找相似序列程序
#==============================================================================
import numpy as np
import pandas as pd
import datetime
import os
import sqlalchemy as sa
# from matplotlib import pyplot as plt

class find_similar(object):
    def __init__(self,code,date,feature_name,step):
        """
        :param code: string
        :param date: datetime.date
        :param feature_name: string
        :param step: int
        """
        rootdir=os.getcwd() + '/servies_model/similar_search'
        path_df=os.path.join(rootdir,'ts_{0}_{1}.pkl'.format(step,feature_name))
        path_df_raw=os.path.join(rootdir,'ts_raw_{0}_{1}.pkl'.format(step,feature_name))
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
        self.ts={'time_series_close':ts_close,'time_series_high':ts_high,'time_series_low':ts_low,
                 'time_series_open':ts_open,'time_series_volume':ts_vol}

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

    def summary(self,close_weight,open_weight,high_weight,low_weight,volume_weight):
        """
        :param close_weight: float
        :param open_weight: float
        :param high_weight: float
        :param low_weight: float
        :param volume_weight:float
        """
        self.df_cos_dis['sum']=self.df_cos_dis['time_series_close_score']*close_weight+self.df_cos_dis['time_series_open_score']*open_weight+self.df_cos_dis['time_series_high_score']*high_weight+self.df_cos_dis['time_series_low_score']*low_weight+self.df_cos_dis['time_series_volume_score']*volume_weight
        self.df_cos_dis.sort_values(by='sum',ascending=False,inplace=True)
        self.result=self.df_cos_dis.iloc[:5]

    # def statis(self,con):
    #     con=con.connect()
    #     lst=[]
    #     for i in range(len(self.result))[1::]:
    #         code=self.result.iloc[i]['code']
    #         trade_date=self.result.iloc[i]['trade_date']
    #         sql='''select p_change from quant_base.stock_data where code='{0}' and trade_date >={1} order by trade_date DESC limit 1'''.format(code,trade_date)
    #         lst.append(pd.read_sql(sql=sql,con=con)['p_change'].values[0])
    #     self.predict=lst
    #     con.close()

    # def plot(self,plot_num=9):
    #     self.df_cos_dis.sort_values(by='time_series_close_score',ascending=False,inplace=True)
    #     df_plot=self.df_cos_dis.head(plot_num)
    #     fig,axes=plt.subplots(3,3)
    #     for i,axe in enumerate(axes.reshape(-1)):
    #         temp=df_plot.iloc[i]
    #         plot_data=self.df_raw[(self.df_raw['code']==temp['code']) & (self.df_raw['trade_date']==temp['trade_date'])]['time_series_close'].values[0]
    #         axe.plot(plot_data)


def search_similar(code, date, feature, step=5, **kwargs):
    """
    :param code: string
    :param date: datetime
    :param feature: string
    :param step: int
    :param kwargs:{'close','open','high','low','volume'}
    :return: (bool,[[code1,code2,code3,code4],[date1,date2,date3,date4]])
    """
    usr = find_similar(code, date, feature, step)
    if not usr.erro:
        usr.count_distance()
        usr.summary(kwargs['close'],kwargs['open'],kwargs['high'],kwargs['low'],kwargs['volume'])
    else:
        return False, 'no data'
    return True, [usr.result['code'].tolist(),usr.result['trade_date'].tolist()]

if __name__=='__main__':
    code='002044'
    date=datetime.date(2017,10,20)
    feature='close'
    step=5
    dic={'close':0.6,'open':0.1,'high':0.1,'low':0.1,'volume':0.1}
    ok, result=search_similar(code, date, feature, step, close=0.6, open=0.1, high=0.1, low=0.1, volume=0.1)
    print result
