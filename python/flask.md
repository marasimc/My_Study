# 1. 设置启动的服务器多线程状态

```python
from flask import Flask

app = Flask(__name__)

app.run(threaded=False)   # 单线程处理请求
app.run(threaded=True)    # 多线程处理请求（默认）
```

测试代码：

```python
import threading
import time
from flask import Flask

app = Flask(__name__)

count = 0
@app.route('/')
def hello_world():
    global count

    count += 1
    if count % 2 == 1:
        print(threading.currentThread().ident, 'sleep 10')    # 输出线程id，是否等待
        time.sleep(10)
    else:
        print(threading.currentThread().ident, 'no sleep')

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
   

### curl http://127.0.0.1:5000/ 进行测试
```

# 2. Get与Post请求

## 2.1 区别：

① get请求：

- 使用场景： 如果只是对服务器获取数据， 并没有对服务器产生任何影响，那么这时候使用get请求
- 传参： get请求传参是放在url中，并且是通过`?`的形式来指定key和value的。

② post请求：

- 使用场景：如果要对服务器产生影响，那么使用post请求。
- 传参： post请求传参不是放在url中，是通过`form data`的形式发送给服务器的。

## 2.2 get和post请求获取参数：

① get请求是通过`flask.request.args`来获取。

② post请求是通过`flask.request.form`来获取。

③ post请求在模板中要注意几点：

- input标签中， 要写那么来表示这个value的key， 方便后台获取。
- 在写form表单的时候， 要指定`method=post`, 并且要指定`action='/login/'`

## 2.3 GET请求

```python
""" 1. 两种参数获取方式 """
from flask import request

request.args.get('key')      # 方式1 
request.values.get('key')    # 方式2

""" 2. 在route装饰器语句中，通过methods指定请求方式 """
@app.route("/", methods=["GET"])

""" 3. 获取参数 """
if request.method == "GET":
    comment = request.args.get("content")
    comment = request.values.get("content")
```

## 2.4 POST请求

客户端在发送`post`请求时，数据可以使用不同的`Content-Type` 来发送：

- 以 `application/json` 的方式 ，请求`body`体的内容就是`{"a": "b", "c": "d"}`
- 以 `application/x-www-form-urlencoded` 的方式，则`body`体的内容就是 `a=b&c=d`

`POST`请求不同`Content-Type`的处理方式：

```python
""" 1. Content-Type为 application/json，获取json参数 """
request.get_json()['content']
# 或者
request.json.get('centent')
# 获取的是序列化后的参数，一般情况下满足使用，不需要json.loads()来序列化。
# 打印出结果就是json串，如{'name':'lucy', 'age':22}


""" 2. Content-Type为 application/json，获取json原始参数 """
request.get_data()
# request.get_data()获取的原始参数，接受的是type是'bytes’的对象，如：b{'name':'lucy', 'age':22}


""" 3. Content-Type为application/x-www-form-urlencoded """
request.values.get('key')


""" 4. Content-Type为multipart/form-data ，获取表单参数 """
request.form.get('key')
# 或者
request.form['key']


""" 5. 例子 """
if request.method == "POST":
     if request.content_type.startswith('application/json'):            
         # comment = request.get_json()["content"]
         comment = request.json.get('content')
     elif request.content_type.startswith('multipart/form-data'):
         comment = request.form.get('content')
     else:
         comment = request.values.get("content")
```

## 2.5 requests模块发送post请求，flask开启服务接收请求

```python
import requests
import json
 
 
if __name__ == '__main__':
    url = 'http://127.0.0.1:5000'
    data = {"imageId": "xxxx", "base64Data": "xxxx", "format": "jpg", "url": "xxxxx"}
    data = json.dumps(data)
    r = requests.post(url, data=data)
    print(r.text)
```

```python
from flask import Flask,request
app = Flask(__name__)
 
 
@app.route("/", methods=["POST"])
def view_func_2():
 
    data = request.get_json()
    if data:
        pass
    else:
        data = request.get_data()
        data = json.loads(data)
 
    imageId = data["imageId"]
    base64Data = data["base64Data"]
    format = data["format"]
    url = data["url"]
 
    print(data)
    print(imageId)
    print(base64Data)
    print(format)
    print(url)
    return "OK"
 
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
```

# 3. flask上下文全局变量

| 变量名      | 上下文     | 说明                                                         |
| ----------- | ---------- | ------------------------------------------------------------ |
| current_app | 程序上下文 | 当前激活的程序实例，比如helloworld例子中的app                |
| g           | 程序上下文 | 用作处理请求时的临时存储，每次请求都重设                     |
| request     | 请求上下文 | 请求对象，包含了客户端HTTP请求的内容，例如获取客户端请求报文头部中包含的<br/>User-Agent信息：request.headers.get("User-Agent") |
| session     | 请求上下文 | 用户会话，字典格式，存储请求间需要记住的信息                 |

# 4. 设置、获取、删除cookie

1. 设置cookie：

```python
'''
设置cookie,默认有效期是临时cookie,浏览器关闭就失效
可以通过 max_age 设置有效期， 单位是秒
'''

resp = make_response("success")  # 设置响应体
resp.set_cookie("Itcast_1", "python_1", max_age=3600)
```

  2.获取cookie

```python
'''
获取cookie，通过reques.cookies的方式， 返回的是一个字典，可以获取字典里的相应的值
'''

cookie_1 = request.cookies.get("Itcast_1")
```

3.删除cookie

```python
'''
这里的删除只是让cookie过期，并不是直接删除cookie
删除cookie，通过delete_cookie()的方式， 里面是cookie的名字
'''

resp = make_response("del success")  # 设置响应体
resp.delete_cookie("Itcast1")
```
eg.

```python
from flask import Flask, make_response, request
 
app = Flask(__name__)
 
 
@app.route("/set_cookie")
def set_cookie():
    resp = make_response("success")
    '''
        设置cookie,默认有效期是临时cookie,浏览器关闭就失效
        可以通过 max_age 设置有效期， 单位是秒
    '''''
    resp.set_cookie("Itcast_1", "python_1")
    resp.set_cookie("Itcast_2", "python_2")
    resp.set_cookie("Itcast_3", "python_3", max_age=3600)
    return resp
 
 
@app.route("/get_cookie")
def get_cookie():
    """
        获取cookie，通过reques.cookies的方式，
        返回的是一个字典，可以用get的方式
    """
    cookie_1 = request.cookies.get("Itcast_1")  # 获取名字为Itcast_1对应cookie的值
    return cookie_1
 
 
@app.route("/delete_cookie")
def delete_cookie():
    """
        删除cookie，通过delete_cookie()的方式，
        里面是cookie的名字
        这里的删除只是让cookie过期，并不是直接删除cookie
    """
    resp = make_response("del success")
    resp.delete_cookie("Itcast1")
    return resp
 
 
if __name__ == '__main__':
    app.run(debug=True)
```

# 5. 并行运行多个flask应用程序

eg.

```python
import threading
from flask import Flask

# ./media is a folder that holds my JS, Imgs, CSS, etc.

app1 = Flask(__name__, static_folder='./media')
app2 = Flask(__name__, static_folder='./media')

@app1.route('/')
def index1():
	return 'Hello World 1'

@app2.route('/')
def index2():
	return 'Hello World 2'

# With Multi-Threading Apps, YOU CANNOT USE DEBUG!
# Though you can sub-thread.
def runFlaskApp1():
	app1.run(host='127.0.0.1', port=5000, debug=False, threaded=True)

def runFlaskApp2():
	app2.run(host='127.0.0.1', port=5001, debug=False, threaded=True)

if __name__ == '__main__':
    # Executing the Threads seperatly.
    t1 = threading.Thread(target=runFlaskApp1)
    t2 = threading.Thread(target=runFlaskApp2)
    t1.start()
    t2.start()
```

# 6. 返回数据

```python
# 方法一：返回一般的字典类型数据
import json

data = {'test': 1}
@app.route('/', methods=['GET'])
def get_tasks():
	return json.dumps({'data':data}, ensure_ascii=False)  # ensure_ascii=False 是为了保证中文显示不乱码
```

```python
# 方法二：返回任意类型的数据，包括列表，字典

from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 保证中文显示不乱码

tasks = [
    {
        'id': 1,
        'title': u'订阅 python_mastery 专栏',
        'description': u'专栏Link： https://xiaozhuanlan.com/python_mastery'
    },
    {
        'id': 2,
        'title': u'订阅 pythonml 专栏',
        'description': u'专栏Link： https://xiaozhuanlan.com/pythonml'
    }
]

@app.route('/', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})
    # return json.dumps({'task:', tasks})

if __name__ == '__main__':
    app.run(debug=True)
```

