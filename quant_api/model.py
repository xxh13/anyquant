# -*- coding:utf-8 -*-

from sqlalchemy import Column, String, Integer, Float, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'
    # 模型与表列对应
    s_id = Column('id', Integer, primary_key=True)
    s_type = Column('type', Integer)
    s_code = Column('code', String(100))
    s_date = Column('date', DateTime)
    s_open = Column('open', Float)
    s_high = Column('high', Float)
    s_low = Column('low', Float)
    s_close = Column('close', Float)
    s_adj_close = Column('adj_price', Float)
    s_volume = Column('volume' ,BigInteger)


class Stock_sha300(Base):
    __tablename__ = 'stock_sha300'
    # 模型与表列对应
    s_id = Column('id', Integer, primary_key=True)
    s_code = Column('code', String(100))
    s_name = Column('name', String(100))
    s_date = Column('date', DateTime)
    s_weight = Column('weight', Float)


class Stock_info(Base):
    __tablename__ = 'stock_info'
    # 模型与表对应
    s_id = Column('id', Integer, primary_key=True)
    s_type = Column('type', Integer)
    s_code = Column('code', String(100))
    s_date = Column('date', DateTime)
    s_turnover = Column('turnover', Float)   #换手率
    s_pe_ttm = Column('pe_ttm', Float)       #市盈率
    s_ps_ttm = Column('ps_ttm', Float)
    s_pc_ttm = Column('pc_ttm', Float)
    s_pb = Column('pb', Float)               #市净率