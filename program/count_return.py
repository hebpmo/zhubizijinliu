# -*- coding: utf-8 -*-
"""
本代码，根据前面(L2_zhubijisuan.py)代码统计出的每天净手数换手率前100名，
或者用(count_top100.py)排序后的结果，根据股票代码，在第二天以上一交易日
收盘价买入，分析其后2、3、5、7天等的收益情况
author: Wang   2018/11/5 14:11
"""
import pandas as pd
import os
import datetime
import time

# pd.set_option('display.max_rows', None)
pd.set_option('expand.frame_repr', False)
start = time.perf_counter()
# ========第一步 首先导入需回测的股票代码========

# 以后可不用移动源数据文件夹，直接改这个日期
'''根据文件名，按天计算'''
os.chdir('E:/L2_result/top100/')  # 或  E:\L2_result\top100_sort文件夹
file_chdir = os.getcwd()

# 读取文件所在目录，获取文件名列表
file_list = []
for root, dirs, files in os.walk(file_chdir):
    for file in files:
        if os.path.splitext(file)[1] == '.csv':
            file_list.append(file[:-4])  # 文件名不包含“.csv”
    # count = len(file_list)
# print(file_list)
# exit()
# ========== 根据上一步得到的文件名列表，提取其中的股票代码，
# 遍历所有股票（暂时先用tushare获取所有日线数据），计算每个股票的收益。
# 先给出日线数据所在路径
file_dir = 'E:/tushare/day_data'
# 读取每个文件，从中提取投票代码，为下面的计算提供股票代码list
output = pd.DataFrame()
for f in file_list:
    # code = f.split()[-1].strip()  # 读取股票代码
    # print(code)
    print(f)
    df = pd.read_csv(file_chdir + '/' + f + '.csv', encoding='gbk')
    df['code'] = df['code'].astype(str).str.zfill(6)
    code_list = df.code.tolist()
    # print(code_list)
    for f in code_list:
        print(f)
        df1 = pd.read_csv(file_dir + '/' + f + '.csv', encoding='gbk')
        # print(df1)
        # exit()
    # exit()
        output = pd.DataFrame()
        df1 = df1.set_index(['trade_date'])  # 如果要计算全天的，则把本行及下面一行屏蔽即可
        start_date = '20180907'
        df1 = df1.loc[start_date:]
        # print(df1)
        # exit()
        # ===== 进入前100名后，第二天以进入当天的收盘价买入，计算其后1, 2, 3, 5, 10, 20与买入当天相比的涨跌情况
        for n in [1, 2, 3, 5, 10, 20]:
            output['其后'+str(n)+'天'] = df1['close'].shift(-1 * n) / df1['close'] - 1.0
            output.dropna(how='any', inplace=True)  # 删除所有有空值的数据行
            
output.to_csv('linshi.csv', encoding='gbk')
print(output)
    # exit()

    