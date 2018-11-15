# -*- coding: utf-8 -*-
"""
本代码，用来从L2数据的计算结果中，提取每只股票、每天的资金流入数据，
用来图形化显示每天的流入流出。
"""
import pandas as pd
import os
import time
import datetime as dt

# pd.set_option('display.max_rows', None)
pd.set_option('expand.frame_repr', False)
start = time.perf_counter()

# =====设置工作目录=====
os.chdir('E:/L2_result/all/')  # 设置源数据目录
file_chdir = os.getcwd()  # 将数据目录设为工作目录
# print(file_chdir)
# exit()

# =====导入股票基本数据，以获得股票列表=====
basic = pd.read_csv('E:/all_python/zhubizijinliu/program/basic.csv', encoding='gbk')
basic['code'] = basic['code'].astype(str).str.zfill(6)
basic = basic[['code', 'name']]
code_list = basic.code.tolist()
# print(code_list)

# 读取CSV文件所在目录，获取文件名列表
file_list = []
for root, dirs, files in os.walk(file_chdir):
    for file in files:
        if os.path.splitext(file)[1] == '.csv':
            file_list.append(file[:-4])  # 文件名不包含“.csv”
    # count = len(file_list)
# print(file_list)
# exit()

output = pd.DataFrame()
# ===遍历每天的CSV文件===

for f in file_list:
    print(f)

    # 读取数据
    file_dir = file_chdir + '/'
    df = pd.read_csv(file_dir + '/' + f + '.csv', encoding='gbk')
    df['code'] = df['code'].astype(str).str.zfill(6)
    # print(df)
    # exit()

    for x in code_list:
        df_temp = df[df['code'] == x]
        # print(df_temp)
        # exit()
        df_temp.to_csv('E:/L2_result/every_stock_L2/' + x + '.csv', mode='a', header=None, encoding='gbk')
        # exit()
end = time.perf_counter()
print(end - start)
