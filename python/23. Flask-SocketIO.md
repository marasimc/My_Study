# 1. 使用指南

## 1.1 初始化

```python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

if __name__ == '__main__':
    # socketio.run()函数封装了 Web 服务器的启动，并替换了app.run()标准的 Flask 开发服务器启动。
    socketio.run(app, host='0.0.0.0', debug=True)
```

## 1.2 连接事件

```python
'''
连接事件处理程序可以选择返回False以拒绝连接。这样就可以在此时对客户端进行身份验证。
请注意，连接和断开连接事件将在使用的每个命名空间上单独发送。
'''
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
```

## 1.3 接收消息

```python
'''
使用 SocketIO 时，双方都会将消息作为事件接收。在客户端使用 Javascript 回调。使用 Flask-SocketIO，服务器需要为这些事件注册处理程序，类似于视图函数处理路由的方式。

socket监听响应函数本身不需要返回什么值，只需要在处理过程中适当的位置emit出消息即可。
'''
##### 未命名事件类型1：使用字符串消息
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
   
##### 为命名事件类型2：使用 JSON 数据
@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
   
##### 类型3：最灵活的方式是使用自定义事件名称，在开发过程中最常用的也是这种方式。事件的消息数据可以是字符串，字节，整数或 JSON
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
   
# 自定义命名事件也可以支持多个参数：
@socketio.on('my event')
def handle_my_custom_event(arg1, arg2, arg3):
    print('received args: ' + arg1 + arg2 + arg3)

# Flask-SocketIO 支持 SocketIO 命名空间，允许客户端在同一物理套接字上复用多个独立连接：
# 如果未指定名称空间，'/'则使用具有名称的默认全局名称空间 。
# socketio用了和app.route类似的装饰器的形式进行监听设置。主要参数中有namespace这一项，也就是这项指定了这个监听的范围。在前端，只有注册在namespace上的socket，emit向request_for_response的消息才会被这个函数接受并处理。
@socketio.on('my event', namespace='/test')
def handle_my_custom_namespace_event(json):
    print('received json: ' + str(json))

# 对于装饰器语法不方便的情况，on_event可以使用该方法：
def my_function_handler(data):
    pass

socketio.on_event('my event', my_function_handler, namespace='/test')

# 客户端可以请求确认回叫，确认收到他们发送的消息。处理函数返回的任何值都将作为回调函数中的参数传递给客户端：
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    return 'one', 2
```

## 1.4 发送消息

```python
'''
可以使用send()和emit() 函数将回复消息发送到连接的客户端。
send()和emit()分别用于无名和命名事件。
'''
from flask_socketio import send, emit

@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('json')
def handle_json(json):
    send(json, json=True)

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)
```

```python
'''
当有命名空间的工作，send()并emit()默认使用传入消息的命名空间。可以使用可选namespace参数指定不同的命名空间
'''
@socketio.on('message')
def handle_message(message):
    send(message, namespace='/chat')

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json, namespace='/chat')

# 要发送具有多个参数的事件，则发送元组：
@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', ('foo', 'bar', json), namespace='/chat')
```

```python
'''
SocketIO 支持确认回调，确认客户端收到了一条消息
使用回调时，Javascript 客户端会收到一个回调函数，以便在收到消息时调用。客户端应用程序调用回调函数后，服务器将调用相应的服务器端回调。如果使用参数调用客户端回调，则这些回调也作为服务器端回调的参数提供。
'''
def ack():
    print 'message was received!'

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json, callback=ack)
```

## 1.5 广播

```python
'''
SocketIO 的另一个非常有用的功能是广播消息。SocketIO 支持通过此功能broadcast=True可选参数send()和emit()

在启用广播选项的情况下发送消息时，连接到命名空间的所有客户端都会接收它，包括发件人。如果未使用名称空间，则连接到全局名称空间的客户端将收到该消息。请注意，不会为广播消息调用回调。
'''
@socketio.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)
```

```python
'''
socketio.send()和socketio.emit()方法可用于广播到所有连接的客户端：
注意：socketio.send()与socketio.emit()在上下文理解上和send()与emit()功能不同
'''
def some_function():
    socketio.emit('some event', {'data': 42})  # 此用法中用法中没有客户端上下文，因此broadcast=True是默认的，不需要指定。
```

## 1.6 房间

```python
'''
所有客户端在连接时都会被分配一个房间，以连接的会话ID命名，可以从中获取request.sid
'''
from flask_socketio import join_room, leave_room

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

```

## 1.7 错误处理

```python
'''错误处理函数将异常对象作为参数。'''
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass

@socketio.on_error('/chat') # handles the '/chat' namespace
def error_handler_chat(e):
    pass

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    pass

'''
还可以使用request.event变量检查当前请求的消息和数据参数，这对于事件处理程序外部的错误记录和调试很有用
'''
from flask import request

@socketio.on("my error event")
def on_my_event(data):
    raise RuntimeError()

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)
```

## 1.8 基于类的命名空间

```python
'''
使用基于类的命名空间时，服务器接收的任何事件都将调度到名为带有on_前缀的事件名称的方法。例如，事件my_event将由名为on_my_event的方法处理(如果收到的事件没有在命名空间类中定义的相应方法，则忽略该事件)
基于类的命名空间中使用的所有事件名称必须使用方法名称中合法的字符。
'''
from flask_socketio import Namespace, emit

class MyCustomNamespace(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_my_event(self, data):
        emit('my_response', data)

socketio.on_namespace(MyCustomNamespace('/test'))

```

## 1.9 测试

```python
''' 脚本 '''
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

name_space = '/dcenter'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/push')
def push_once():
    event_name = 'dcenter'
    broadcasted_data = {'data': "test message!"}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    return 'done!'


@socketio.on('connect', namespace=name_space)
def connected_msg():
    print('client connected.')


@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    print('client disconnected.')


@socketio.on('my_event', namespace=name_space)
def mtest_message(message):
    print('message:', message)
    emit('my_response',
         {'data': message['data'], 'count': 1})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SocketIO Demo</title>
    <script type="text/javascript" src="//cdn.bootcss.com/jquery/3.1.1/jquery.min.js"></script>
    <script type="text/javascript" src="//cdn.bootcss.com/socket.io/3.0.0/socket.io.min.js"></script>
</head>
<body>

<h2>Demo of SocketIO</h2>
<div id="t"></div>
<script>
$(document).ready(function () {
    namespace = '/dcenter';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('dcenter', function (res) {
        var t = res.data;
        if (t) {
            $("#t").append(t).append('<br/>');
        }
    });
});
</script>
</body>
</html>
```

