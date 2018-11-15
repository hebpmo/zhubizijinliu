# -*- coding: utf-8 -*-
"""
@author:     2018/9/5 15:44
"""
import os
import  time
import pandas as pd
import numpy as np
from program import config
from program import Functions
pd.set_option('display.max_rows', None)
start = time.clock()

# ===================================================
# 第一步 首先按日期导入逐笔数据
# 1、遍历数据文件夹中所有股票文件的文件名，得到股票文件名列表file_list

file_list = []
for root, dirs, files in os.walk(config.input_data_path):  # 注意：这里请填写数据文件在您电脑中的路径
    if files:
        for f in files:
            if '.csv' in f:
                file_list.append(f.split('.csv')[0])


# ========== 根据上一步得到的文件名列表，遍历所有股票，计算每个股票的资金流数据，放入output变量
output = pd.DataFrame()

# ===遍历每个股票
for f in file_list:
    code = f.split()[-1].strip()  # 读取股票代码
    print code
    # exit()

    stock_data = pd.read_csv(config.input_data_path + '/' + 'zhubi-' + f[:10] + '/' + f + '.csv',
                             parse_dates=[0])  # 注意：这里请填写数据文件在您电脑中的路径，注意斜杠方向
    stock_data.columns = [i.encode('utf8') for i in stock_data.columns]

    stock_data['Money'] = stock_data['Volume'] * stock_data['Price']  # 计算每笔交易成交额

    l = len(output)
    output.loc[l, 'code'] = code
    output.loc[l, '平均每笔交易成交量'] = stock_data['Volume'].mean()

    # 计算资金流入流出
    data = stock_data.groupby('BuySell')['Money'].sum()
    if 'B' in data.index:
        output.loc[l, '资金流入'] = data['B']
        # if output['资金流入'] == 0:
        #     pass
    if 'S' in data.index:
        output.loc[l, '资金流出'] = data['S']
    output.loc[l, '净流入'] = int((output.loc[l, '资金流入'] - output.loc[l, '资金流出']) / 10000)  # 此行为王增加

    # 计算主力资金流入流出
    data = stock_data[stock_data['Volume'] > 50000].groupby('BuySell')['Money'].sum()
    if 'B' in data.index:
        output.loc[l, '主力资金流入'] = data['B']
    if 'S' in data.index:
        output.loc[l, '主力资金流出'] = data['S']
    output.loc[l, '主力资金净流入'] = int((output.loc[l, '主力资金流入'] - output.loc[l, '主力资金流出']) / 10000)  # 此行为王增加

# ========== 输出每个股票的资金流数据到csv文件，用中文excel或者wps打开查看
filedate = file_list[0]
filedate = filedate[:10]

output.to_csv(config.output_data_path + '/' + str(filedate) + '.csv', mode='w', index=False, encoding='gbk')

# output.to_hdf('zijin.h5', 'output', index=False, mode='w')  # 经过努力，保存成h5成功，关键是后面要加上 'output' 这一项。
# 以后可在里面加上路径。目前是保存在.py所在目录。
end = time.clock()
print '计算用时',
print end -  start
