import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif']=['SimHei']

# 读取RFM.csv文件
df = pd.read_csv('RFM.csv')
# 统计四种用户的数量
user_counts = df['User_Label'].value_counts()
# 计算占比
user_percentages = user_counts / len(df) * 100
# 打印统计结果
print("用户统计：")
print(user_counts)
print("\n用户占比：")
print(user_percentages)
# 可视化不同用户的占比（饼图）
plt.figure(figsize=(12, 6))
plt.pie(user_percentages, labels=user_percentages.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("viridis"))
plt.title("不同用户类型占比")
plt.show()
# 可视化不同用户的数量（柱状图）
plt.figure(figsize=(10, 6))
sns.barplot(x=user_counts.index, y=user_counts.values, palette="viridis")
plt.title("不同用户类型数量统计")
plt.xlabel("用户类型")
plt.ylabel("数量")
for i, v in enumerate(user_counts.values):
    plt.text(i, v + 0.1, str(v), ha='center', va='bottom', fontproperties='SimHei', fontsize=10)
plt.show()