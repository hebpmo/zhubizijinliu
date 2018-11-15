# -*- coding: utf-8 -*-
"""
这是系列计算的第二步
本代码，把已完成的L2top_100('E:/L2_result/top100/')，按5天一组循环分组
输出到E:/L2_result/top100_5day/
author: Wang   2018/10/31 9:26
2018/11/07备忘：
在循环5天一组的代码中，增加了判断文件是否存在的语句：if file exists，跳过。（或者，采用追加记录的方式）
不再重复写文件。参见博闻视频。
"""
import pandas as pd
import os
import time
import datetime
from _datetime import datetime

# pd.set_option('display.max_rows', None)
pd.set_option('expand.frame_repr', False)
start = time.perf_counter()

# ======================

os.chdir('E:/L2_result/top100/')
file_chdir = os.getcwd()

# 1、=====读取文件所在目录，获取文件名列表======
file_list = []
for root, dirs, files in os.walk(file_chdir):
    for file in files:
        if os.path.splitext(file)[1] == '.csv':
            file_list.append(file[:-4])  # 文件名不包含“.csv”
    count = len(file_list)
# print(file_list)
# exit()

# 2、============分组读入文件合并后保存==============
a = file_list
a.sort(reverse=True)
index = a.index(a[-1])
for date in a:
    df = pd.DataFrame()
    if index < 4:
        break
    b = [a[index - i] for i in range(5)]
    # print(b)
    for j in b:
        print(j)
        df = df.append(pd.read_csv(file_chdir + '/' + str(j) + '.csv', encoding='gbk'))
    # 判断文件是否存在：if file exists，跳过
    file = 'E:/L2_result/top100_5day/' + str(j) + '.csv'
    if os.path.exists(file):
        pass
    else:
        df.to_csv('E:/L2_result/top100_5day/' + str(j) + '.csv', encoding='gbk')
    # print(df)
    index -= 1
# exit()
end = time.perf_counter()
print(end - start)




