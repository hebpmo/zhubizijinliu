# -*- coding: utf-8 -*-
"""
这是系列计算的第三步
本代码，从已完成的5天的净手数100名文件(E:/L2_result/top100_5day/），
统计各股票连续5天中，按股票出现次数从多到少排序
author: Wang   2018/11/2 12:54
"""
import pandas as pd
import os
import time

# pd.set_option('display.max_rows', None)
pd.set_option('expand.frame_repr', False)
start = time.perf_counter()
# ========第一步 首先按日期导入逐笔数据========

# 以后可不用移动源数据文件夹，直接改这个日期，但应注意星期天无数据
os.chdir('E:/L2_result/top100_5day/')
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
# ========== 根据上一步得到的文件名列表，遍历所有股票，计算每个股票的资金流数据，放入output变量
# output = pd.DataFrame()
# i = '2018-10-18'  # 以后计算时，可以不用移动源数据文件夹，直接改这个日期应该就可以
i = file_chdir[-10:]
# ===遍历每个股票

for f in file_list:
    # print(f)
    df = pd.DataFrame()
    # 读取数据
    file_dir = file_chdir + '/'
    df = pd.read_csv(file_dir + '/' + f + '.csv', encoding='gbk')
    # df = pd.read_csv('E:/L2_result/top100_5day/2018-11-02.csv', encoding='gbk')
    df['code'] = df['code'].astype(str).str.zfill(6)
    # df = df[['日期', 'code', 'name', '收盘价', '换手率']]
    list1 = df.code.value_counts()  # 本行可输出统计个数，但还没有办法通过code把它利用起来，
    list2 = list1.index.tolist()
    # print(f)
    # exit()
# print(list2)
# exit()
df1 = pd.DataFrame()
for j in list2:
    print(j)
    df = pd.read_csv(file_dir + '/' + f + '.csv', encoding='gbk')
    # df = pd.read_csv('E:/L2_result/top100_5day/2018-11-02.csv', encoding='gbk')
    df['code'] = df['code'].astype(str).str.zfill(6)
    df1 = df1.append(df[(df['code'].isin([j]))])
# df1 = df1.iloc[0:100]  # 本来想取前100名，后来想，有的是第一天进入前100，后面可能还会进，就全部输出。
df1.to_csv('E:/L2_result/top100_sort/' + str(f) + '.csv', encoding='gbk')
end = time.perf_counter()
print(end - start)
