# -*- coding: utf-8 -*-
"""
本代码，根据选出的前100只股票，
author: Wang   DATE:2018/11/15 TIME:16:40
"""
import pandas as pd
import os
import datetime as dt

# pd.set_option('display.max_rows', None)
pd.set_option('expand.frame_repr', False)
times1 = dt.datetime.now()

# =====设置工作目录=====
os.chdir('E:/L2_result/top100/')  # 从前100中取股票进行验证
file_chdir = os.getcwd()
file_dir = 'E:/tushare/day_data/'  # 股票日线数据文件夹

# ====读最后一天的  top100  股票代码====
today = dt.date.today()  # 此为   class 'datetime.date'  格式
yesterday = today - dt.timedelta(days=1)  # class 'datetime.date'  格式，可以直接加减，几天都行。
print('今天是：' + str(today))
print('读入  ' + str(yesterday) + '  的前100名')

df = pd.read_csv(str(yesterday) + '.csv', encoding='gbk')  # 这里还需要转换成 str 格式。
df['code'] = df['code'].astype(str).str.zfill(6)


# =====读取数据通过匹配的股票代码=======
def code_filter(code):
    """如果股票连续5天涨幅超过-1且小于5，返回True，否则返回False"""
    start = today - dt.timedelta(days=7)  # 实际为5个交易日
    start1 = str(start)
    # print(code)  # 如果不想看到数据输出，可以屏蔽这行。
    df1 = pd.read_csv(file_dir + code + '.csv', encoding='gbk')
    df1['trade_date'] = pd.to_datetime(df1['trade_date'],  format='%Y%m%d')  # 这行有用，不能删
    df1.set_index("trade_date", inplace=True)
    df2 = df1.loc[start1:]
    # print(df2)  # 如果不想看到数据输出，可以屏蔽这行。
    
    continue_num_of_value_want = 0
    for v in df2['pct_change']:
        if -1 < v < 5:
            continue_num_of_value_want += 1
        else:
            continue_num_of_value_want = 0
        if continue_num_of_value_want >= 5:
            return True
    return False


# 根据题主条件筛选出的股票列表
code_list = df.code.tolist()
codes_wanted = [code for code in code_list if code_filter(code)]
print(codes_wanted)

times2 = dt.datetime.now()
print('用时: ' + str(times2 - times1))
