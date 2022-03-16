# numpy用法

## 1. ndarray

array: 一维数组

ndarray: 多维数组

```html
ndarray.ndim：数组的维数，在Python中叫做rank
ndarray.shape： 数组的维数。它是一组长度由数组维数(ndim)决定的数字。例如，长度为n的一维数组的形状是n，而n行m列的数组的形状shape是(n,m)。
ndarray.size：数组中所有元素的数量。
ndarray.dtype：数组中元素的类型，如numpy.int32、numpy.int16或numpy.float64。
ndarray.itemsize：数组中每个元素的大小，以字节为单位
ndarray.data：用于存储数组元素的缓冲。通常我们只需要通过下标来访问元素，而不需要访问缓冲区。
```

```python
import numpy as np

b = np.array([(1,2,3), (4,5,6)])

print('b=')
print(b)
print("b's ndim {}".format(b.ndim))           # 2
print("b's shape {}".format(b.shape))         # (2,3)
print("b's size {}".format(b.size))           # 6
print("b's dtype {}".format(b.dtype))         # int32
print("b's itemsize {}".format(b.itemsize))   # 4
```

也可以在创建数组时指定元素的类型，例如:

```python
c = np.array( [ [1,2], [3,4] ], dtype=complex )
```

## 2. list 与 np.array()的区别

```tex
python 中的 list 是 python 的内置数据类型，list 中的数据类型不必相同，
在 list 中保存的是数据的存放的地址，即指针，并非数据。

array() 是 numpy 包中的一个函数，array 里的元素都是同一类型。
np.array()可以将 Python 的任何序列类型转换为 ndarray 数组。

python中 list 与数组array的互相转换：
① list转array：np.array(a)
② array 转list：a.tolist()
```

```python
import numpy as np

l = [[1,2,3],[4,5,6]]
l_arr = np.array(l)
print('l_arr', l_arr)

l_1 = l_arr.tolist()
print('l_1:', l_1)
```

## 3. 创建特定数组

```text
zeros：
ones：
empty：
arange：
linespace：
random
```

```python
import numpy as np

a = np.zeros((2,3))
print('np.zeros((2,3)= \n{}\n'.format(a))

b = np.ones((2,3))
print('np.ones((2,3))= \n{}\n'.format(b))

c = np.empty((2,3))
print('np.empty((2,3))= \n{}\n'.format(c))

d = np.arange(1, 2, 0.3)
print('np.arange(1, 2, 0.3)= \n{}\n'.format(d))

e = np.linspace(1, 2, 7)
print('np.linspace(1, 2, 7)= \n{}\n'.format(e))

f = np.random.random((2,3))
print('np.random.random((2,3))= \n{}\n'.format(f))
```

## 4. 形状和操作

```tex
除了生成数组之外，在保存了一些数据之后，还可能需要基于现有数组生成一些新的数据结构。

reshape：用于基于现有数组和指定形状生成新数组，就是重塑行列
vstack：用于在垂直方向上堆叠多个数组(数组的维度必须匹配)
hstack：用于水平方向堆叠多个数组(数组的维度必须匹配)
hsplit：用于水平分割数组
vsplit：用于垂直分割数组
```

```python

```

## 5. index

```python
''' 对于一维数组 '''
import numpy as np

base_data = np.arange(100, 200)

### 1. 下标为单个数
print(base_data[10])

### 2. 下标为一维数组
every_five = np.arange(0, 100, 5)
print(base_data[every_five])

### 3. 下标为多维数组
a = np.array([(1,2), (10,20)])
print(base_data[a])  #得到的结果为二维数组
```

```python
''' 对于二维数组 '''
import numpy as np

base_data = np.arange(100, 200)
base_data = np.reshape(base_data, (10,-1))

# 如果只指定一个下标，访问的结果仍然是一个数组。
# 如果指定两个下标，则访问的结果是内部的元素。
# 还可以通过“-1”指定最后一个元素。
```

## 6. 数学计算

```python
import numpy as np

base_data = (np.random.random((5, 5)) - 0.5) * 100
np.amin(base_data)     # 取最小值
np.amax(base_data)     # 取最大值
np.average(base_data)  # 取均值
np.sum(base_data)      # 求和
np.sin(base_data)      # 对于base_data中的每一个元素求sin
```

```python
import numpy as np

arr = np.arange(1,20)   # [1,2,3,4,...,19]
arr = arr * arr         # [1,4,9,....361]
arr = arr - arr         # [0,0,0...0]

arr = np.arange(1,20)
arr = arr + arr         # [2,4,6,....38]
arr = arr / arr         # [1. 1. ...]

arr = np.arange(1,20)
arr = arr + 50          # [51,52...]
```

```python
import numpy as np

np.sqrt(arr)
np.exp(arr)
np.sin(arr)
np.cos(arr)
np.log(arr)
np.sum(arr)
np.std(arr)
```

```python
import numpy as np

base_data = np.floor((np.random.random((5, 5)) - 0.5) * 100)    # np.floor()是对输入的多维数组进行向下取整

# 转置
base_data.T   或者    base_data.transpose()

# 点乘
matrix_one = np.ones((5, 5))
minus_one = np.dot(matrix_one, -1)
np.dot(base_data, minus_one)
```

## 8. 随机数

```python
import numpy as np

np.random.random(20)                   # 生成20个随机数，每个随机数在[0,1)之间
np.random.rand(3, 4)                   # 根据指定的形状生成随机数，[0,1)之间
np.random.randint(0, 100, 20)          # 生成指定范围内(如[0,100)的指定个数(如20)的随机整数
np.random.permutation(np.arange(20)    # 将现有数据([0,1,2，…， 19])随机打乱
```

