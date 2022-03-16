**1、创建Excel**

```python
import xlwt

stus =  [
    ['姓名','年龄','性别','分数'],
    ['cm',18,'女',100],
    ['cm1',18,'女',100],
    ['cm2',18,'女',100],
    ['cm3',18,'女',100],
]
book = xlwt.Workbook()#新建excel文件
sheet = book.add_sheet('sheet1') #新建sheet
row = 0  # 循环写列
for stu in stus:
    col = 0
    for s in stu:
        sheet.write(row,col,s)
        col+=1
    row+=1
    
book.save('stu1.xlsx') #保存名称
```

**2、读取Excel：xlrd**

```python
import xlrd # 读取Excel

book = xlrd.open_workbook('stu1.xlsx') #打开excel
sheet = book.sheet_by_index(0) #根据顺序获取sheet页
# sheet = book.sheet_by_name(0) #根据名称获取sheet页
print(sheet.cell(0,0).value) #指定行和列获取数据
print(sheet.cell(1,0).value) #指定行和列获取数据
print(sheet.ncols) #获取excel里面有多少列
print(sheet.nrows) #获取excel里面有多少列
print(sheet.row_values(1))#取第几行的数据
print(sheet.col_values(1))#取第几行的数据
#输出每行的数据
for i in range(sheet.nrows):
    print(sheet.row_values(i))
```

 **3、修改Excel：xlutlis**

```python
import xlutils #修改Excel
import xlrd
from xlutils.copy import copy

bookl = xlrd.open_workbook('stu1.xlsx')
book2 = copy(bookl) #拷贝一份原来的excel
sheet = book2.get_sheet(0) #获取第几个shheet页
sheet.write(1,3,0) #将第二行第四列修改成0
book2.save('stu_new.xlsx')
```

***reference: https://www.1024sou.com/article/76711.html***