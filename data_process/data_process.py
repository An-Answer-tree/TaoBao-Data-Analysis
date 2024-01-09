import pandas

# 数据集导入
df = pandas.read_csv('./user_action.csv')
print('最初数据：\n', df.head(), '\n\n')
print('最初数据类型：\n', df.dtypes, '\n\n')


# 数据预处理
# 在df中去除有空值的数据项，并在原地修改
df.dropna(axis=0, how='any', inplace=True)

# 在df中去除所有字段相同的重复值，保留第一个
# print(df.drop_duplicates(ignore_index=True))

# 将df中time字段删除，增加mon，day，hour三个字段
df['mon'] = df['time'].str.split(pat='-', expand=True)[1]
df['day'] = df['time'].str.split(pat='-', expand=True)[2]
df['hour'] = df['time'].str.split(pat=' ', expand=True)[1]
df.drop(labels='time', axis=1, inplace=True)
print('当前数据：\n', df.head(), '\n\n')
print('当前df数据类型：\n', df.dtypes, '\n\n')