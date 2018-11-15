# -*- coding: utf-8 -*-
"""
这是系列计算的第一步
本代码，用来计算全天（也可根据L2数据前30分钟）的成交数据，
统计出买入和卖出的手数、资金流入流出量，计算出净手数换手率，
分别输出全部股票(E:/L2_result/all)及净手数换手率前100名(E:/L2_result/top100)。
Author: Wang  2018/10/27 19:56
2018/11/07：昨天应翰墨缘要求增加了“资金净流入”一列，但在下一个环节，
即5天一组的代码运行中，出现了列不相符的警告，暂时解决不了，故先把该列输出屏蔽，等以后有能力时再说。
"""
import pandas as pd
import os
import time
import datetime as dt

# pd.set_option('display.max_rows', None)
pd.set_option('expand.frame_repr', False)
start = time.perf_counter()
# times1 = dt.datetime.now()

# =====导入股票基本数据=====
basic = pd.read_csv('basic.csv', encoding='gbk')
basic['code'] = basic['code'].astype(str).str.zfill(6)
basic = basic[['code', 'name', 'outstanding']]
# print(basic)
# exit()

# ========第一步 首先按日期导入逐笔数据========

# 以后可不用移动源数据文件夹，直接改这个日期，但应注意星期天无数据
os.chdir('E:/2018_tick_data/201811/2018-11-14')
file_chdir = os.getcwd()

# 读取文件所在目录，获取文件名列表
file_list = []
for root, dirs, files in os.walk(file_chdir):
    for file in files:
        if os.path.splitext(file)[1] == '.csv':
            file_list.append(file[:-4])  # 文件名不包含“.csv”
    # count = len(file_list)
# exit()
# ========== 根据上一步得到的文件名列表，遍历所有股票，计算每个股票的资金流数据，放入output变量
output = pd.DataFrame()
# i = '2018-10-18'  # 以后计算时，可以不用移动源数据文件夹，直接改这个日期应该就可以
i = file_chdir[-10:]
# ===遍历每个股票
for f in file_list:
    # code = f.split()[-1].strip()  # 读取股票代码
    # print(code)
    print(f)

    # 读取数据
    file_dir = file_chdir + '/'
    df = pd.read_csv(file_dir + '/' + f + '.csv', encoding='gbk')
    # print(df)
    '''
    df['日期'] = df['成交时间'].str.split(' ').str[0]  # 本行分离出日期
    df['时间'] = df['成交时间'].str.split(' ').str[1]  # 本行分离出时间
    df = df[['日期', '时间', '成交价格', '成交数量', '主动买卖属性']]
    # print(df)
    # 把9:30~10:00之间的数据重新组成一个新的DateFrame
    t = pd.to_datetime(df.时间)
    df = df[(t >= '09:30:00') & (t <= '10:00:00')]
    # print(df)
    '''
    # ===========另一方法取时间段========
    # df.index = pd.to_datetime(df['成交时间'])  # 如果要计算全天的，则把本行及下面一行屏蔽即可
    # df = df[i + ' 09:25:00': i + ' 09:38:00']
    # print(df)
    # exit()
    # ====================
  
    # 对新的DateFrame，根据买、卖分组统计。
    
    df['成交金额'] = df['成交数量'] * df['成交价格']  # 计算每笔交易成交额

    #  计算平均每笔交易成交量
    m = len(output)
    try:
        output.loc[m, 'code'] = f
        output.loc[m, '每笔均量'] = df['成交数量'].mean()
        output.loc[m,'收盘价'] = df.iat[-1, 1]
    except:
        pass
    # print(output)
    # exit()
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
    output.loc[m, '资金净流入'] = output.loc[m, '资金流入'] - output.loc[m, '资金流出']
    output.loc[m, '净手数'] = output.loc[m, '买入手数'] - output.loc[m, '卖出手数']
    filedate = file_chdir[-10:]
    output['日期'] = filedate
    output = output[['日期', 'code', '收盘价',  '每笔均量', '资金流入', '买入手数', '资金流出', '卖出手数', '净手数']]
    # output = output[['日期', 'code', '收盘价',  '每笔均量', '资金流入', '买入手数', '资金流出', '卖出手数', '净手数', '资金净流入']]
    # output['code'] = [i[2:] for i in output['code']]  # 从SH600000和SZ000260中提取非字母代码
    # df = pd.merge(left=output, right=basic, on='code', how='left', sort=True, indicator=True)
    # df['turnover'] = (df.买入手数 + df.卖出手数) / (df.outstanding * 100000000) * 10000
    # print(output)
    # exit()
output['code'] = [i[2:] for i in output['code']]
df = pd.merge(left=output, right=basic, on='code', how='left', sort=True, indicator=True)
df['换手率'] = df.净手数 / df.outstanding / 100
# df['资金流入'] = df['资金流入'].sum()  #本行及下面2行，就是计算资金净流入的，取消屏蔽即可显示
# df['资金流出'] = df['资金流出'].sum()
# df['资金净流入'] = df['资金流入'] - df['资金流出']
# df['turnover'] = (df.买入手数 + df.卖出手数) / (df.outstanding * 100000000) * 10000
df.drop(['_merge'], axis=1, inplace=True)

df = df[['日期', 'code',  'name', '收盘价', '每笔均量', '资金流入', '买入手数', '资金流出', '卖出手数', '净手数', '换手率']]
# df = df[['日期', 'code',  'name', '收盘价', '每笔均量', '资金流入', '买入手数', '资金流出', '卖出手数', '净手数', '换手率', '资金净流入']]
# df = df.sort_values(by=['换手率'],  ascending=0, inplace=True)
df.sort_values(by=['换手率'],  ascending=0, inplace=True)
filedate = file_chdir[-10:]
df.to_csv('E:/L2_result/all/' + filedate + '.csv', encoding='gbk', mode='w', index=False)
df = df.iloc[0:100]
# print(df)
# exit()
# df.to_csv(file_chdir[:-21] + '/output_data/' + filedate + '.csv', encoding='gbk', mode='w', index=False)
df.to_csv('E:/L2_result/top100/' + filedate + '.csv', encoding='gbk', mode='w', index=False)
print(filedate + '.csv' + '  已保存')
end = time.perf_counter()
print(end - start)
