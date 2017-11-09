# -*- coding: utf-8 -*-
#==============================================================================
#寻找相似序列程序
#==============================================================================
import numpy as np
import pandas as pd
import datetime
import os
import sqlalchemy as sa

class find_similar(object):
    def __init__(self,code,date,feature_name,step):
        """
        :param code: string
        :param date: datetime.date
        :param feature_name: string
        :param step: int
        """
        rootdir=os.getcwd() + '/servies_model/similar_search'
        #rootdir=os.getcwd()
        path_df=os.path.join(rootdir,'ts_{0}.pkl'.format(step))
        label_name='label_{}'.format(feature_name)
        df=pd.read_pickle(path_df)
        try:
            label=df[(df['code']==code) & (df['trade_date']==date)][label_name].values[0]
            ts_close=df[(df['code']==code) & (df['trade_date']==date)]['time_series_close'].values[0]
            ts_open=df[(df['code']==code) & (df['trade_date']==date)]['time_series_open'].values[0]
            ts_high=df[(df['code']==code) & (df['trade_date']==date)]['time_series_high'].values[0]
            ts_low=df[(df['code']==code) & (df['trade_date']==date)]['time_series_low'].values[0]
            ts_vol=df[(df['code']==code) & (df['trade_date']==date)]['time_series_volume'].values[0]
            self.erro=False
        except:
                self.erro=True
                return
        self.df=df[df[label_name]==label]
        self.ts={'time_series_close':ts_close,'time_series_high':ts_high,'time_series_low':ts_low,
                 'time_series_open':ts_open,'time_series_volume':ts_vol}

    @staticmethod
    def cos_dis(x,y):
        return np.dot(x,y)

    def count_distance(self):
        cos_dis_dict={'code':[],'trade_date':[],'time_series_close_score':[],'time_series_open_score':[],'time_series_high_score':[],'time_series_low_score':[],'time_series_volume_score':[]}
        for i in range(len(self.df)):
            for col in self.df.columns[1:6]:
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
    date=datetime.date(2017,10,18)
    feature='low'
    step=3
    dic={'close':0.6,'open':0.1,'high':0.1,'low':0.1,'volume':0.1}
    ok, result=search_similar(code, date, feature, step, close=0.6, open=0.1, high=0.1, low=0.1, volume=0.1)
    print result
