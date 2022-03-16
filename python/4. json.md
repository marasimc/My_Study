用法：

```python
import json

""" 
1. json.loads() : 将 JSON 对象转换为 Python 字典
"""

""" 
2. json.dumps() : 将 Python 字典类型转换为 JSON 对象
"""

"""
3. json.load() # 将一个存储在文件中的json对象（str）转化为相对应的python对象
"""

"""
4. json.dump() # 将python的对象转化为对应的json对象（str),并存放在文件中
"""
```

例子：

```python
#!/usr/bin/python3
import json
 
# Python 字典类型转换为 JSON 对象
data1 = {
    'name' : 'Runoob',
    'url' : 'http://www.runoob.com'
}
 
json_str = json.dumps(data1)
print ("Python 原始数据：", repr(data1))
print ("JSON 对象：", json_str)
 
# 将 JSON 对象转换为 Python 字典
data2 = json.loads(json_str)
print ("data2['name']: ", data2['name'])
print ("data2['url']: ", data2['url'])


"""
json.loads(json_str)中，
在windows平台下json_str可以是byte类型！
但是Linux下必须str类型！
"""
```

```python
import json

# 读取json文件内容,返回字典格式
with open('./source_file/info.json','r',encoding='utf8')as fp:
    json_data = json.load(fp)
    print('这是文件中的json数据：',json_data)
    print('这是读取到文件数据的数据类型：', type(json_data))
    
    
# 将字典数据写入到json文件中
dict1 = {'name': '张三', 'age': 18, 'sex': '男'}
with open('./source_file/info.json','a',encoding='utf8')as fp:
    json.dump(dict1,fp,ensure_ascii=False)　　
 #  如果ensure_ascii ' '为false，则返回值可以包含非ascii值
```

