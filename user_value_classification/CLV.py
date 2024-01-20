import pandas as pd
import os

if not os.path.exists("Lifespan.csv"):
    # 读取原始数据
    df = pd.read_csv('E:\Programming_Tool\Project\Python\TaoBao-Data-Analysis\DATA\\user_action.csv')
    # 将时间列转换为 datetime 类型
    df['time'] = pd.to_datetime(df['time'])
    # 计算每个用户的第一次行为时间和最后一次行为时间
    user_first_last_time = df.groupby('user_id')['time'].agg(['min', 'max']).reset_index()
    user_first_last_time.columns = ['user_id', 'first_time', 'last_time']
    # 计算时间差
    user_first_last_time['行为时间差'] = (
                user_first_last_time['last_time'] - user_first_last_time['first_time']).dt.days
    # 计算行为次数
    user_behavior_count = df.groupby('user_id')['behavior_type'].count().reset_index()
    user_behavior_count.columns = ['user_id', '行为次数']
    # 合并结果
    result_df = pd.merge(user_first_last_time[['user_id', '行为时间差']], user_behavior_count, on='user_id')
    # 保存结果为csv文件
    result_df.to_csv('Lifespan.csv', index=False)

if not os.path.exists("Goods_Scores.csv"):
    # 读取原始数据
    df = pd.read_csv('../DATA/user_action.csv')
    # 计算每个item_id的总得分
    item_scores = df.groupby('item_id')['behavior_type'].sum().reset_index()
    # 以item_id为主码生成新的DataFrame
    new_df = pd.DataFrame({'item_id': item_scores['item_id'], 'item_scores': item_scores['behavior_type']})
    # 确保item_id是唯一且非空的主码
    new_df = new_df.dropna(subset=['item_id']).drop_duplicates(subset=['item_id'])
    # 保存新数据为csv文件
    new_df.to_csv('Goods_Scores.csv', index=False)

check = pd.read_csv('Goods_Scores.csv')
if '商品价值' not in check.columns :
    # 添加"商品价值"列根据条件编码
    check['商品价值'] = check.cut(check['item_scores'], bins=[-float('inf'), 5, 9, float('inf')], labels=[1, 2, 3])
    # 保存修改后的数据为csv文件
    check.to_csv('Goods_Scores.csv', index=False)

df = pd.read_csv("CLV.csv")
if '商品价值' not in df.columns :
    df = pd.read_csv("../DATA/Target.csv")
    # 合并两个数据框，根据item_id进行匹配
    df = pd.merge(df, check[['item_id', '商品价值']], on='item_id', how='left')
    # 保存修改后的数据为csv文件
    df.to_csv('CLV.csv', index=False)

# 读取 CLV.csv、RFM.csv 和 Lifespan.csv 文件
clv = pd.read_csv('CLV.csv')
Lifespan = pd.read_csv('Lifespan.csv')
RFM = pd.read_csv('RFM.csv')

# 计算每个用户的商品价值平均值 AOV
user_aov = clv.groupby('user_id')['商品价值'].mean().reset_index()
user_aov.columns = ['user_id', 'AOV']
# 合并 AOV 和 Lifespan
result_df = pd.merge(Lifespan, user_aov, on='user_id', how='left')
# 处理 RFM 中的异常值，将列表转换为整数
RFM['user_id'] = RFM['user_id'].apply(lambda x: int(x[1:-1]) if isinstance(x, str) and x.startswith('[') and x.endswith(']') else x)
# 将 RFM 中的 user_id 列转换为整数
RFM['user_id'] = RFM['user_id'].astype(int)
# 合并 RFM
result_df = pd.merge(result_df, RFM, on='user_id', how='left')
# 保存结果为 csv 文件
result_df.to_csv('CLV_final.csv', index=False)