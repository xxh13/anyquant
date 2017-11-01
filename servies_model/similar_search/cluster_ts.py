# -*- coding: utf-8 -*-
#==============================================================================
#时间序列聚类程序
#==============================================================================
import numpy as np
import sqlalchemy as sa
import pandas as pd
import sklearn.cluster

class cluster_ts(object):
    def __init__(self,con,feature_name):
        '''
        feature_name为需要聚类的属性名字，这里我们主要取close,open,volume,high,low
        '''
        sql='select code,trade_date,close,open,volume,high,low from quant_base.stock_data'
        self.stock_data=pd.read_sql(sql=sql,con=con)
        self.stock_data.set_index('code',inplace=True)
        self.code_set=set(self.stock_data.index)
        self.feature_name=feature_name

    def split_time_series(self,step=5,gap=1):
        '''
        分割时间序列，进行l2处理
        step:时间序列长度
        gap:取的间隔
        '''
        self.step=step
        time_series={'code':[],'trade_date':[],'time_series_close':[],'time_series_open':[],'time_series_high':[],'time_series_low':[],'time_series_volume':[]}
        time_series_raw={'code':[],'trade_date':[],'time_series_close':[],'time_series_open':[],'time_series_high':[],'time_series_low':[],'time_series_volume':[]}
        for code in self.code_set:
            temp=self.stock_data.loc[code]
            lst_ts_close=[(temp.iloc[i:i+step]['close']/np.linalg.norm(temp.iloc[i:i+step]['close'])).tolist() for i in range(0,len(temp)-step,gap)]
            lst_ts_close_raw=[(temp.iloc[i:i+step]['close']).tolist() for i in range(0,len(temp)-step,gap)]
            lst_ts_open=[(temp.iloc[i:i+step]['open']/np.linalg.norm(temp.iloc[i:i+step]['open'])).tolist() for i in range(0,len(temp)-step,gap)]
            lst_ts_open_raw=[(temp.iloc[i:i+step]['open']).tolist() for i in range(0,len(temp)-step,gap)]
            lst_ts_high=[(temp.iloc[i:i+step]['high']/np.linalg.norm(temp.iloc[i:i+step]['high'])).tolist() for i in range(0,len(temp)-step,gap)]
            lst_ts_high_raw=[(temp.iloc[i:i+step]['high']).tolist() for i in range(0,len(temp)-step,gap)]
            lst_ts_low=[(temp.iloc[i:i+step]['low']/np.linalg.norm(temp.iloc[i:i+step]['low'])).tolist() for i in range(0,len(temp)-step,gap)]
            lst_ts_low_raw=[(temp.iloc[i:i+step]['low']).tolist() for i in range(0,len(temp)-step,gap)]
            lst_ts_volume=[(temp.iloc[i:i+step]['volume']/np.linalg.norm(temp.iloc[i:i+step]['volume'])).tolist() for i in range(0,len(temp)-step,gap)]
            lst_ts_volume_raw=[(temp.iloc[i:i+step]['volume']).tolist() for i in range(0,len(temp)-step,gap)]
            lst_code=[code]*len(lst_ts_close)
            lst_date=[temp.iloc[i].trade_date for i in range(0,len(temp)-step,gap)]
            time_series['code']+=lst_code
            time_series['trade_date']+=lst_date
            time_series['time_series_close']+=lst_ts_close
            time_series['time_series_open']+=lst_ts_open
            time_series['time_series_high']+=lst_ts_high
            time_series['time_series_low']+=lst_ts_low
            time_series['time_series_volume']+=lst_ts_volume
            time_series_raw['code']+=lst_code
            time_series_raw['trade_date']+=lst_date
            time_series_raw['time_series_close']+=lst_ts_close_raw
            time_series_raw['time_series_open']+=lst_ts_open_raw
            time_series_raw['time_series_high']+=lst_ts_high_raw
            time_series_raw['time_series_low']+=lst_ts_low_raw
            time_series_raw['time_series_volume']+=lst_ts_volume_raw
        self.df=pd.DataFrame(time_series)
        self.df_raw=pd.DataFrame(time_series_raw)

    def cluster(self,center_num):
        '''
        计算每个时间序列的标签
        center_num:聚类数量
        '''
        self.kmeans=sklearn.cluster.KMeans(n_clusters=center_num,max_iter=1000,n_jobs=-1)
        self.kmeans.fit(self.df['time_series_'+self.feature_name].tolist())
        self.df['label']=self.kmeans.labels_
        self.df_raw['label']=self.kmeans.labels_

    def save(self):
        self.df.to_pickle('ts_{0}_{1}.pkl'.format(self.step,self.feature_name))
        self.df_raw.to_pickle('ts_raw_{0}_{1}.pkl'.format(self.step,self.feature_name))

if __name__=='__main__':
    con=sa.create_engine('mysql://quant:quant@120.27.199.164/quant_base').connect()
    for feature in ['close','open','high','low','volume']:
        for step in [3,5,7,9]:
            cluster=cluster_ts(con,'close')
            cluster.split_time_series(step=step)
            cluster.cluster(1000)
            cluster.save()
    con.close()
