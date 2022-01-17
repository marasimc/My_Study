xlrd和xlwt模块主要是针对excel表格的读取和写入，但是一些操作和处理数据的操作还是需要根据xlutils这个模块来实现。

# 1. 拷贝原文件

```python
import xlrd
from xlutils.copy import copy


workbook = xlrd.open_workbook('test.xlsx')  # 打开工作薄
new_workbook = copy(workbook)  # 将获取的xlrd文件对象，拷贝为xlwt对象
new_workbook.save('new_test.xlsx')  # 保存工作薄
```

# 2. 拷贝前获取原工作薄的信息

```python
workbook = xlrd.open_workbook('test.xlsx')     # 打开工作簿

sheets = workbook.sheet_names()                # 获取工作簿中的所有工作表名字，形成列表元素
worksheet = workbook.sheet_by_name(sheets[0])  # 通过sheets[0]工作表名称获取工作簿中所有工作表中的的第一个工作表
rows_old = worksheet.nrows                     # 获取第一个工作表中已存在的数据的行数

print(sheets, sheets[0], worksheet, worksheet.nrows)
```

# 3. 拷贝后获取新工作薄的信息

```python
workbook = xlrd.open_workbook('test.xlsx')  # 打开工作簿

new_workbook = copy(workbook)               # 将xlrd对象拷贝转化为xlwt对象
new_worksheet = new_workbook.get_sheet(0)   # 获取转化后工作簿中的第一个工作表对象

print(new_worksheet, new_workbook, new_worksheet.name)  # 有时间整理下工作表对象的方法,工作表可以.name
```

# 4. 拷贝后直接修改文件内容

```python
# 打开想要更改的excel文件
old_excel = xlrd.open_workbook('test.xlsx', formatting_info=True)

# 将操作文件对象拷贝，变成可写的workbook对象
new_excel = copy(old_excel)
# 获得第一个sheet的对象
ws = new_excel.get_sheet(0)
# 写入数据
ws.write(0, 0, '第一行，第一列')
ws.write(0, 1, '第一行，第二列')
ws.write(0, 2, '第一行，第三列')
ws.write(1, 0, '第二行，第一列')
ws.write(1, 1, '第二行，第二列')
ws.write(1, 2, '第二行，第三列')
# 另存为excel文件，并将文件命名，可以重新命名，应该也可以覆盖掉
new_excel.save('new_test_1.xlsx')
```

# 5. 获取所有单元格索引坐标

```python
workbook = xlrd.open_workbook('test.xlsx')  # 打开工作簿

Data_sheet = workbook.sheets()[0]

row1 = Data_sheet.row_values(0)  # 取出第一行
dic_col_s = {str(i): row1[i] for i in range(0, len(row1))}  # 将第一行的每个元素加个序数标记，标记列表索引，让列表索引和标题对应，由标题则可以从字典获取列号，即列表索引+1，这里需要的是索引

col2 = Data_sheet.col_values(0)  # 取出第一列，
dic_row_s = {str(i): col2[i] for i in range(0, len(col2))}  # 将第一列的每个元素加个序数标记，标记为第一列的列表索引。让名字和列表索引对应，就可以在字典中由名字得行号，即列表索引+1。这里需要的是这个索引

mtitle = "gender"  # 需要修改哪个标题
mname = "tank"     # 需要修改哪个人的
rindex = "".join([i for i in dic_row_s if dic_row_s[i] == mname])  # 获取要修改的标题所在行的索引
cindex = "".join([i for i in dic_col_s if dic_col_s[i] == mtitle])  # 获取要修改的那个人所在的列索引

print(f"rindex:{rindex},cindex:{cindex}")

---------------------------------执行结果-------------------------------------
{'0': 'name', '1': 'class', '2': 'cid', '3': 'gender'}
{'0': 'name', '1': 'sean', '2': 'tank', '3': 'jason'}
rindex:2,cindex:3
```

