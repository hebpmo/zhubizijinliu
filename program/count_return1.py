# -*- coding: utf-8 -*-
"""
author: Wang   2018/11/7 8:30
本代码，根据前面(L2_zhubijisuan.py)代码统计出的每天净手数换手率前100名，
或者用(count_top100.py)排序后的结果，根据股票代码，在第二天以上一交易日
收盘价买入，分析其后2、3、5、7天等的收益情况
20181115  目前代码还有问题，计算不是从需要它开始的日期，而是从有数据以来
"""
import pandas as pd
import os
import datetime as dt
import time
from datetime import datetime, timedelta

# pd.set_option('display.max_rows', None)
pd.set_option('expand.frame_repr', False)
times1 = dt.datetime.now()

# =====设置工作目录=====
os.chdir('E:/L2_result/top100/')  # 从前100中取股票进行验证
file_chdir = os.getcwd()
file_dir = 'E:/tushare/day_data'  # 股票日线数据文件夹

# ======确定开始计算的日期======
today = dt.date.today()  # 此为   class 'datetime.date'  格式
start = today - dt.timedelta(days=21)  # 实际为5个交易日
start1 = str(start)
print('今天是：' + str(today))
print('读入  ' + str(start) + '  的前100名')

df = pd.read_csv(str(start) + '.csv', encoding='gbk')  # 这里还需要转换成 str 格式。
df['code'] = df['code'].astype(str).str.zfill(6)
code_list = df.code.tolist()
# print(df)
# exit()

# print(code_list)
# exit()

# =====读入要计算的CSV文件=====
output = pd.DataFrame()
for f in code_list:
    print(f)
    # exit()
    #
    df1 = pd.read_csv(file_dir + '/' + f + '.csv', encoding='gbk')
    df1['trade_date'] = pd.to_datetime(df1['trade_date'], format='%Y%m%d')  # 这行有用，不能删
    df1.set_index("trade_date", inplace=True)
    
    df1 = df1.loc[start1:]
    # print(df1)
    # exit()
    # ===== 进入前100名后，第二天以进入当天的收盘价买入，计算其后1, 2, 3, 5, 10, 20与买入价相比的涨跌情况
    # for n in [1, 2, 3, 5, 10, 20]:  # 计算10、20天用处不大，暂时不算它。
    for n in [1, 2, 3, 5]:
        output['其后' + str(n) + '天'] = (df1['close'].shift(-1 * n) / df1['close'] - 1.0) * 100
        output.dropna(how='any', inplace=True)  # 删除所有有空值的数据行
    print(output)
    time.sleep(3)
    output.to_csv('E:/linshi_data/00/' + f + '.csv', encoding='gbk')


times2 = dt.datetime.now()
print('Time spent: ' + str(times2 - times1))

