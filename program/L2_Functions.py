# -*- coding: utf-8 -*-
"""
此代码，将计算L2的各步骤，分开，写成函数
author: Wang   2018/10/29 9:26
"""
import pandas as pd
import os
import time
import tushare as ts
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', None)

# path = 'E:/all_python/zhubizijinliu/data/input_data/2018-10-18'

# =====导入股票基本数据=====
basic = pd.read_csv('basic.csv', encoding='gbk')
basic['code'] = basic['code'].astype(str).str.zfill(6)
basic = basic[['code', 'name', 'outstanding', ]]
print(basic)
exit()

# =====读取文件所在目录，获取文件名列表=====
def dirlist(path):
    """
    :param path: 本函数，使用时，需要用一个变量，如下行
     allfile = dirlist('E:/all_python/zhubizijinliu/data/input_data/2018-10-18')
     或直接引用，如：print(dirlist('E:/all_python/zhubizijinliu/data/input_data/2018-10-18'))
    :return:
    """
    filelist = os.listdir(path)
    allfile = []
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.splitext(filepath)[-1] == '.csv':
                allfile.append(filepath[-12:-4])  # 文件名不包含“.csv”
        # print(allfile)
    return allfile


# list = dirlist('E:/all_python/zhubizijinliu/data/input_data/2018-10-18')
# list1 = dirlist(path)
# print(list1)


def data_30min(path):
    """
    # ========== 根据上一步得到的文件名列表，遍历所有股票，计算每个股票的资金流数据，放入output变量
    """
    output = pd.DataFrame()
    file_dir = os.path.realpath(path)
    # ===遍历每个股票
    for f in dirlist(path):
        print(f)
        
        # 读取数据
        df = pd.read_csv(str(file_dir) + '/' + f + '.csv', encoding='gbk')
        # print(df)
        # exit()
        
        df['日期'] = df['成交时间'].str.split(' ').str[0]  # 本行分离出日期
        df['时间'] = df['成交时间'].str.split(' ').str[1]  # 本行分离出时间
        df = df[['日期', '时间', '成交价格', '成交数量', '主动买卖属性']]
        # print(df)

        # 把9:30~9:40之间的数据重新组成一个新的DateFrame
        # t = pd.to_datetime(df.时间)
        # df = df[(t >= '09:30:00') & (t <= '10:00:00')]
        # print(df)
    
        # 对新的DateFrame，根据买、卖分组统计。
    
        df['成交金额'] = df['成交数量'] * df['成交价格']  # 计算每笔交易成交额
    
        #  计算平均每笔交易成交量
        m = len(output)
        output.loc[m, 'code'] = f
        output.loc[m, '每笔均量'] = df['成交数量'].mean()
    
        data = df.groupby('主动买卖属性')['成交金额'].sum()
        data1 = df.groupby('主动买卖属性')['成交数量'].sum()
    
        # 统计买入
        if 'B' in data.index:
            output.loc[m, '资金流入'] = data['B'].astype('int64')  # 后面的代码是取消科学计数显示
            output.loc[m, '买入手数'] = data1['B'].astype('int64')  # 后面的代码是取消科学计数显示
    
        # 统计卖出
        if 'S' in data.index:
            output.loc[m, '资金流出'] = data['S'].astype('int64')
            output.loc[m, '卖出手数'] = data1['S'].astype('int64')
        output.loc[m, '净手数'] = output.loc[m, '买入手数'] - output.loc[m, '卖出手数']
        filedate = file_dir[-10:]
        output['日期'] = filedate
        output = output.sort_values(by=['净手数'], ascending=0)
        output = output[['日期', 'code',  '每笔均量', '资金流入', '买入手数', '资金流出', '卖出手数', '净手数']]
        # print(output)
        # exit()
    return output
    # filedate = file_chdir[-10:]
    # output.to_csv('E:/all_python/zhubizijinliu/data/output_data/' + filedate + '.csv', encoding='gbk', mode='w', index=False)
    output['code'] = [i[2:] for i in output['code']]
    df = pd.merge(left=output, right=basic, on='code', how='left', sort=True, indicator=True)
    df['turnover'] = (df.买入手数 + df.卖出手数) / (df.outstanding * 100000000) * 10000

# out = data_30min(path)
# print(out)

