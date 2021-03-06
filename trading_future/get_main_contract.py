# coding=utf-8
from __future__ import division
import pandas as pd
import datetime
from trading_future.future_singleton import Future
from jqdatasdk import *
from configDB import *
auth(JOINQUANT_USER, JOINQUANT_PW)


def get_date(calen, today):
    next_tradeday = get_trade_days(start_date=today + datetime.timedelta(days=1), end_date='2030-01-01')[0]
    if datetime.datetime.now().hour >= 15:
        calen.append(next_tradeday)
    EndDate = calen[-1]
    StartDate = calen[0]
    hq_last_date = calen[-2]
    return calen, next_tradeday, EndDate, StartDate, str(hq_last_date)[:10]


if __name__ == '__main__':
    symbol_lst = ['C', 'CS', 'A', 'B', 'M', 'RM', 'Y', 'P', 'OI', 'L', 'V', 'PP', 'TA', 'RU', 'BU', 'MA', 'SC', 'FU',
                   'AL', 'ZN', 'CU', 'PB', 'NI', 'SN', 'J', 'JM', 'I', 'RB', 'HC', 'ZC', 'SF', 'SM', 'FG', 'IF',
                   'IH', 'IC', 'T', 'TF', 'AG', 'AU', 'JD', 'AP', 'CJ', 'CF', 'SR']
    symbol_lst = ['SF', 'P', 'CF', 'M', 'OI', 'JD', 'V', 'AP', 'SM', 'RB', 'HC', 'MA', 'FU', 'ZC', 'BU', 'C', 'PP']
    # symbol_lst = ['V', 'AP', 'SM', 'RB', 'HC', 'MA', 'FU', 'ZC', 'TA', 'BU', 'C']
    date = datetime.date.today()
    # date = pd.to_datetime('2020-06-29')

    bars = 5
    calen = get_trade_days(end_date=date, count=bars)
    calen = list(calen)
    print(calen)
    calen, next_tradeday, EndDate, StartDate, hq_last_date = get_date(calen, date)
    porfolio = Future()
    print(EndDate)
    # df = porfolio.get_main_symbol(product=symbol_lst, date=EndDate)
    # print(df)
    df = {}
    for symbol in symbol_lst:
        # print(symbol)
        df[symbol] = [get_dominant_future(symbol, date)]
    df = pd.DataFrame(df).T
    print(df)
    # df.to_csv('c:/g/trading/main_contract.csv')




