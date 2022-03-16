# 1. 系统操作

```python
'''
os.sep         获取系统路径的分隔符（window--'\\'; Linux--'/'）
os.name        指明当前python运行所在的环境（window--’nt‘; Linux/Unix--'posix'）
os.getenv(环境变量名)   读取环境变量
os.getcwd()            获取当前路径
'''

import os
 
print (os.sep)
print (os.name)
print (os.getenv('path'))
print (os.getcwd())
```

# 2. 目录操作

```python
'''
os.listdir('path'):返回指定目录下的所有文件和目录名
os.mkdir('dirname'):创建一个目录
os.rmdir('dirname'):删除一个空目录，若目录中有文件则无法删除
os.makefirs(dirname):可以生成多层递归目录，若目录全部存在，则创建目录失败
os.removedirs(dirname):可以删除多层递归的空目录，若目录中有文件则无法删除
os.chdir():改变当前目录到指定目录中。
os.rename():重命名目录名或文件名。若重命名后的文件名已存在则重命名失败
'''
```

# 3. 判断

```python
'''
os.path.exists(path)
os.path.isfile(path)
os.path.isdir(path)
os.path.isabs(path)
'''
```

# 4. 文件信息

```python
'''
os.path.basename(path): 返回文件名
os.path.dirname(path): 返回文件路径
os.path.getsize(name): 返回文件大小
os.path.abspath(name): 获取绝对路径
os.path.join(path, name): 连接目录与文件名或目录
'''
```

```python
import os
#coding:utf-8
#列出当前目录下的所有文件
dirs="D:\\Release\\bin"
if os.path.exists(dirs):
    files= os.listdir(dirs)
    print(files)
    
    #拼接了路径
    fullpath=os.path.join(dirs,files[0])
    print(fullpath)
    
    #判断一个路径是否是一个文件，是否目录
    if os.path.isfile(fullpath):
        print('我是一个文件')
    elif os.path.isdir(fullpath):
        print('我是一个目录')
```

# 5. 重启程序

```python
import os
import numpy as np
import cv2

THS_name = '同花顺(v9.10.20) - 1号方案'

def restart_THS():
    def is_same(img1, img22):
        image1 = (cv2.imread(img1))[500:1000,:]
        image2 = (cv2.imread(img22))[500:1000,:]
        difference = cv2.subtract(image1, image2)
        # print(difference)
        result = not np.any(difference) #if difference is all zeros it will return False
        
        return result

    try:
        # 关闭原程序
        os.system('taskkill /f /t /im '+'hexin.exe')
    except:
        pass
	#启动进程
    os.startfile(r"C:/同花顺软件/同花顺/hexin.exe")

    test = Win_api_handler(THS_name)
    t1 = time.time()
    while True:
        try: 
            hwnd = test.get_hwnd()
            # time.sleep(1)
            test.window_capture(hwnd, 'page_1.png')

            if is_same('page.png', 'page_1.png'):   # 对比正常启动后的图片与当前截取到的图片，来判断是否已经完成启动
                break
        except:
            pass

    print('用时：', time.time()-t1)
```

