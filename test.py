# coding=utf-8
'''
Created on 9.30, 2018
适用于btc/usdt，btc计价并结算
@author: fang.zhang
'''
from __future__ import division
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pymongo
import datetime
import copy
import math
from arctic import Arctic, TICK_STORE, CHUNK_STORE
style.use('ggplot')
from jqdatasdk import *

import copy
from configDB import *
auth(JOINQUANT_USER, JOINQUANT_PW)
import datetime
import talib as tb
import pymongo
from arctic import Arctic, TICK_STORE, CHUNK_STORE

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from smtplib import SMTP_SSL


def values_data_cgo(stockcode, count, eday):
    """
    输入 股票代码，查询中止日，以及查询多少条数据
    输出 dataframe 市值表 字段为 code :股票代码  day:日期  capitalization:总股本（万股）
    circulating_cap ：流通股本（万股） market_cap：总市值（亿） circulating_market_cap：流通市值（亿）
    turnover_ratio：换手率 pe_ratio：市盈率 TTM pe_ratio_lyr：静态市盈率  pb_ratio：市净率
    ps_ratio：市销率  pcf_ratio：市现率
    """
    q = query(valuation.code,
              valuation.turnover_ratio,
              ).filter(valuation.code == stockcode)

    df = get_fundamentals_continuously(q, count=count, end_date=eday, panel=False)[
        ['day', 'code', 'turnover_ratio']]

    today = datetime.date.today()
    temp = get_price(stockcode, start_date=today, end_date=today, frequency='daily', fields=None, skip_paused=True,
                     fq='post', count=None).reset_index() \
        .rename(columns={'index': 'day'})
    volume = temp.volume.tolist()[-1] * 100 * 100
    q1 = query(finance.STK_CAPITAL_CHANGE.code,
               finance.STK_CAPITAL_CHANGE.change_date,
               finance.STK_CAPITAL_CHANGE.share_trade_total).filter(finance.STK_CAPITAL_CHANGE.code == stockcode)
    circulating_cap = finance.run_query(q1).sort_values(['change_date']).share_trade_total.tolist()[-1] * 10000
    df_today = pd.DataFrame({'day': [today], 'code': [stockcode], 'turnover_ratio': [volume/circulating_cap]})
    ret = []
    ret.append(df[['day', 'code', 'turnover_ratio']])
    ret.append(df_today)
    ret = pd.concat(ret)
    return ret


def stock_price(sec, sday, eday):
    """
    输入 股票代码，开始日期，截至日期
    输出 个股的后复权的开高低收价格
    """
    temp = get_price(sec, start_date=sday, end_date=eday, frequency='daily', fields=None, skip_paused=True, fq='pre',
                     count=None).reset_index() \
        .rename(columns={'index': 'date_time'}) \
        .assign(date_time=lambda df: df.date_time.apply(lambda x: str(x)[:10]))
    return temp


if __name__ == '__main__':
    code_lst = ['RU1609', 'RU1701', 'RU1709', 'RU1801', 'RU1809', 'RU1901', 'RU1909', 'RU2001', 'RU2009', 'RU2101']
    code_lst = [i + '.XSGE' for i in code_lst]
    couple_lst = []
    for i in range(0, len(code_lst), 2):
        couple_lst.append((code_lst[i], code_lst[i+1]))
    s_date = '2016-01-01'
    e_date = '2020-06-01'
    ret = []
    for (code09, code01) in couple_lst:
        hq09 = stock_price(code09, s_date, e_date).assign(close09=lambda df: df.close)[['date_time', 'close09']]
        hq01 = stock_price(code01, s_date, e_date).assign(close01=lambda df: df.close)[['date_time', 'close01']]
        diff = hq09.merge(hq01, on=['date_time']).assign(date=lambda df: df.date_time.apply(lambda x: x[5:]))
        diff['date' + code09[2:4]] = diff['date_time'].apply(lambda x: x[5:])
        diff['20' + code09[2:4]] = diff['close09'] - diff['close01']
        ret.append(diff[['date' + code09[2:4], '20' + code09[2:4]]])
    ret = pd.concat(ret, axis=1)[['date16', '2016', '2017', '2018', '2019', '2020']].rename(columns={'date16': 'date_time'})
    print(ret)
    ret = ret.set_index(['date_time'])
    ret.to_csv('G://zf//RU_09_01.csv')
    ret.ix[:, ['2020', '2019', '2018', '2017', '2016']].plot()
    plt.show()



