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
for row in df.iterrows():
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

- iteritems():按列遍历，将DataFrame的每一列迭代为(列名, Series)对，可以通过row[index]对元素进行访问。

```python
for index, row in df.iteritems():
    print(index)                    # 输出列名
'''
c1
c2
'''    

for row in df.iteritems():
    print(row[0], row[1], row[2])   # 输出各列   
'''
10 11 12
100 110 123
'''    
```

