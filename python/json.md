用法：

```python
""" 
1. json.loads() : 将 JSON 对象转换为 Python 字典
"""

""" 
2. json.dumps() : 将 Python 字典类型转换为 JSON 对象
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

