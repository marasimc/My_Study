# 1. 创建df

```python
import pandas as pd

① 方式一：
inp = [{'c1':10, 'c2':100}, {'c1':11, 'c2':110}, {'c1':12, 'c2':123}]
df = pd.DataFrame(inp)

② 方式二：
c1 = [10, 11, 12]
c2 = [100, 110. 123]
df = pd.DataFrame({'c1': c1, 'c2': c2})


print(df)

'''
   c1   c2
0  10   100
1  11   110
2  12   123
'''
```



# 2. 遍历df

- iterrows(): 按行遍历，将DataFrame的每一行迭代为(index, Series)对，可以通过row[name]对元素进行访问。

```python
for index, row in df.iterrows():
    print(index)                   # 输出每行的索引值
'''
0
1
2
'''    

# 对于每一行，通过列名name访问对应的元素
for index, row in df.iterrows():
    print(row['c1'], row['c2'])     # 输出每一行
'''
10   100
11   110
12   123
'''
```

- itertuples(): 按行遍历，将DataFrame的每一行迭代为元祖，可以通过row[name]对元素进行访问，比iterrows()效率高。

```python
for row in df.itertuples():
    print(getattr(row, 'c1'), getattr(row, 'c2')) # 输出每一行
```

- iteritems():按列遍历，将DataFrame的每一列迭代为(列名, Series)对。

```python
for col_index, col_values in df.iteritems():
    print(index)                    # 输出列名
'''
c1
c2
'''    

for col_index, col_values in df.iteritems():
    print(col_values)   # 输出各列   
'''
10 11 12
100 110 123
'''    
```

# 3. df使用map(),apply(),applymap()函数

```python
'''① map()函数'''
#i. 使用字典进行映射，把数据集中gender列的男替换为1，女替换为0
data["gender"] = data["gender"].map({"男":1, "女":0})


#ii.使用函数，把数据集中gender列的男替换为1，女替换为0
def gender_map(x):
    gender = 1 if x == "男" else 0
    return gender
#注意这里传入的是函数名，不带括号
data["gender"] = data["gender"].map(gender_map)
```

```python
'''② apply()函数主要用于对DataFrame中的某一column或row中的元素执行相同的函数操作。'''
# 对C1列中的每一个元素加1
df["C1"].apply(lambda x:x+1)
# 对第1行的每一个元素加1
df.loc[1].apply(lambda x:x+1)
# 对df表中的每一个元素加1
df.apply(lambda x:x+1)


def apply_age(x,bias):
    return x+bias
#以元组的方式传入额外的参数
data["age"] = data["age"].apply(apply_age,args=(-3,))


## DataFrame中axis的概念:axis=0代表操作对列columns进行，axis=1代表操作对行row进行
# 沿着0轴求和
data[["height","weight","age"]].apply(np.sum, axis=0)
# 沿着0轴取对数
data[["height","weight","age"]].apply(np.log, axis=0)
```

```python
'''③ applymap()函数用于对DataFrame中的每一个元素执行相同的函数操作。'''
# 对df表中的每一个元素加1
df.applymap(lambda x:x+1)
```

# 4. DataFrame新增列的方法

```python
import pandas as pd

data = pd.DataFrame()

''' 1. insert()方法 '''
data.insert(data.shape[1], 'd', [0,0])

''' 2. obj[‘col’] = value 方法 '''
data['d'] = [0,0]

''' 3. reindex 方法 '''
data = data.reindex(columns=['a', 'b', 'c', 'd'], fill_value=0)

''' 4. concat 方法 '''
data = pd.concat([data, pd.DataFrame(columns=['d'])], sort=False)

''' 5. loc 方法 '''
data.loc[:, 'd'] = 0
```

