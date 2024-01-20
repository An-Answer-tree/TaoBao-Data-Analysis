import pandas as pd
import os
#目标文件生成
if not os.path.exists("E:\Programming_Tool\Project\Python\TaoBao-Data-Analysis\DATA\Target.csv"):
    # 数据集导入
    df = pd.read_csv('E:\Programming_Tool\Project\Python\TaoBao-Data-Analysis\DATA\\user_action.csv')
    # 数据预处理
    # 在df中去除有空值的数据项，并在原地修改
    df.dropna(axis=0, how='any', inplace=True)
    # 将time列转换为时间类型
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H')
    # 筛选出behavior_type为4的数据
    target_data = df[df['behavior_type'] == 4]
    #去除不必要列behavior_type
    target_data =target_data.drop('behavior_type', axis=1)
    # 导出修改后的文件
    target_data.to_csv('E:\Programming_Tool\Project\Python\TaoBao-Data-Analysis\DATA\Target.csv', index=False)

if not os.path.exists("E:\Programming_Tool\Project\Python\TaoBao-Data-Analysis\DATA\\RFM.csv"):
    # 数据集导入
    df = pd.read_csv('E:\Programming_Tool\Project\Python\TaoBao-Data-Analysis\DATA\\Target.csv')
    # 数据集按用户的 id 进行分组
    UserAction = df.groupby(by='user_id')
    # 先创建一个空的 DataFrame 存储 R、F 度量
    RFM = pd.DataFrame(index=UserAction['user_id'].unique(), columns=['R', 'F'])
    # 计算与用户购买次数，即 F 指标
    RFM['F'] = UserAction.size()
    # 先统计最后一次日期，再计算 R 指标（设基准为2014.12.31）
    RFM['last_time'] = pd.to_datetime(UserAction.time.max())
    RFM['R'] = (pd.to_datetime('2014-12-31') - RFM['last_time']).dt.days
    # 舍弃无用维度 last_time
    RFM = RFM.drop("last_time", axis=1)
    RFM.to_csv("E:\Programming_Tool\Project\Python\TaoBao-Data-Analysis\DATA\\RFM.csv")

Cal = pd.read_csv("../DATA/RFM.csv")
if 'Rscore' not in Cal.columns or 'Fscore' not in Cal.columns:
    # 统计 RFM 用户群体特征
    avg_R = Cal['R'].mean()
    avg_F = Cal['F'].mean()
    # 完成 R/F 到 Rscore/Fscore 的映射
    Cal['Rscore'] = Cal['R'].apply(lambda x: 1 if x > avg_R else 0)
    Cal['Fscore'] = Cal['F'].apply(lambda x: 1 if x > avg_F else 0)
    # 将Rscore和Fscore拼接为RFM属性列
    Cal['RFM'] = Cal['Rscore'].astype(str) + Cal['Fscore'].astype(str)
    # 将Rscore和Fscore保存为新的维度
    Cal.to_csv('RFM.csv', index=False)
# 创建用户标签属性列User_Label
Cal['User_Label'] = Cal['RFM'].replace({'00': '重要挽留客户', '01': '重要保持客户', '10': '重要发展客户', '11': '重要价值客户'})
# 将用户标签保存为新的维度
Cal.to_csv('RFM.csv', index=False)

