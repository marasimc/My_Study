# 1. 连接MongoDB

```python
import pymongo

'''method_1'''
client = pymongo.MongoClient(host='localhost', port=27017)

'''method_2'''
client = MongoClient('mongodb://localhost:27017/')
```

# 2. 指定数据库

```python
'''method_1'''
db = client.test

'''method_2'''
db = client['test']
```

# 3. 指定集合

```python
'''method_1'''
collection = db.students

'''method_2'''
collection = db['students']
```

# 4. 插入数据

```python
## 插入单条数据
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

result = collection.insert_one(student)
print(result.inserted_id)    # 返回_id值 5932a68615c2606814c91f3d

## 插入多条数据
student1 = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

student2 = {
    'id': '20170202',
    'name': 'Mike',
    'age': 21,
    'gender': 'male'
}

result = collection.insert_many([student1, student2])
print(result.inserted_ids)   
```

# 5. 查询

```python
## 查询单条数据
result = collection.find_one({'name': 'Mike'})
print(type(result))   # <class 'dict'>
print(result)

## 查询多条数据
results = collection.find({'age': 20})
print(results)
for result in results:
    print(result)
```

```python
results = collection.find({'age': {'$gt': 20}})
results = collection.find({'name': {'$regex': '^M.*'}})
results = collection.find({'_id': {"$gt": start_date, "$lt": end_date}}).sort('_id', pymongo.ASCENDING)   # 升序排序
```

| 符号 | 含义       | 示例                        |
| :--- | :--------- | :-------------------------- |
| $lt  | 小于       | {'age': {'$lt': 20}}        |
| $gt  | 大于       | {'age': {'$gt': 20}}        |
| $lte | 小于等于   | {'age': {'$lte': 20}}       |
| $gte | 大于等于   | {'age': {'$gte': 20}}       |
| $ne  | 不等于     | {'age': {'$ne': 20}}        |
| $in  | 在范围内   | {'age': {'$in': [20, 23]}}  |
| $nin | 不在范围内 | {'age': {'$nin': [20, 23]}} |

| 符号    | 含义           | 示例                                              | 示例含义                       |
| :------ | :------------- | :------------------------------------------------ | :----------------------------- |
| $regex  | 匹配正则表达式 | {'name': {'$regex': '^M.*'}}                      | name以M开头                    |
| $exists | 属性是否存在   | {'name': {'$exists': True}}                       | name属性存在                   |
| $type   | 类型判断       | {'age': {'$type': 'int'}}                         | age的类型为int                 |
| $mod    | 数字模操作     | {'age': {'$mod': [5, 0]}}                         | 年龄模5余0                     |
| $text   | 文本查询       | {'$text': {'$search': 'Mike'}}                    | text类型的属性中包含Mike字符串 |
| $where  | 高级条件查询   | {'$where': 'obj.fans_count == obj.follows_count'} | 自身粉丝数等于关注数           |

# 6. 计数

```python
count = collection.find().count()
print(count)

count = collection.find({'age': 20}).count()
print(count)
```

# 7. 排序

```python
"""
pymongo.ASCENDING   表示升序
pymongo.DESCENDING  表示降序
"""
results = collection.find().sort('name', pymongo.ASCENDING)
print([result['name'] for result in results])
```

# 8. 偏移

```python
'''可以利用skip()方法偏移几个位置，比如偏移2，就忽略前两个元素，得到第三个及以后的元素'''
results = collection.find().sort('name', pymongo.ASCENDING).skip(2)
print([result['name'] for result in results])

'''可以用limit()方法指定要取的结果个数'''
results = collection.find().sort('name', pymongo.ASCENDING).skip(2).limit(2)
print([result['name'] for result in results])

'''值得注意的是，在数据库数量非常庞大的时候，如千万、亿级别，最好不要使用大的偏移量来查询数据，因为这样很可能导致内存溢出。此时可以使用类似如下操作来查询：'''
from bson.objectid import ObjectId
collection.find({'_id': {'$gt': ObjectId('593278c815c2602678bb2b8d')}})s
```

# 9. 更新

```python
'''更新一条数据'''
condition = {'name': 'Kevin'}
student = collection.find_one(condition)
student['age'] = 25
result = collection.update_one(condition, student)
print(result)
print(result.matched_count, result.modified_count)

'''更新多条数据'''
condition = {'age': {'$gt': 20}}
result = collection.update_many(condition, {'$inc': {'age': 1}})
print(result)
print(result.matched_count, result.modified_count)
```

# 10. 删除

```python
result = collection.remove({'name': 'Kevin'})
print(result)

'''推荐采用的方法'''
result = collection.delete_one({'name': 'Kevin'})
print(result)
print(result.deleted_count)
result = collection.delete_many({'age': {'$lt': 25}})
print(result.deleted_count)
```



# 11. 其他操作

```python
find_one_and_delete()
find_one_and_replace()
find_one_and_update()

create_index()
create_indexes()
drop_index()
```

