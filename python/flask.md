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

