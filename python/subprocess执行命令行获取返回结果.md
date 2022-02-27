#  subprocess

subprocess 模块允许我们启动一个新进程，并连接到它们的输入/输出/错误管道，从而获取返回值。 

Popen 是 subprocess的核心，子进程的创建和管理都靠它处理。

```python
import subprocess
p = subprocess.Popen('pip -V',
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     )

# 输出stdout
print(p.communicate()[0])
```

```python
import subprocess
p = subprocess.Popen('pip -V',
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     encoding='utf-8'
                     )

# 输出stdout
print(p.communicate()[0])
```

```python
import subprocess
p = subprocess.Popen('java',
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     encoding='gb2312'
                     )

# 输出stdout
print(p.communicate()[0])
```

```python
import subprocess
p = subprocess.Popen(['python', 'xx.py'],
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     encoding='utf-8'
                     )

''' 方式一：实时输出 '''
while p.poll() is None:
    print(p.stdout.readline())

''' 方式二：一次性输出 '''
# 输出stdout
print(p.communicate()[0])
```

