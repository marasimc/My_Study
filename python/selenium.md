# selenium教程

## 1. 安装

```python
pip install selenium
```

安装驱动，放在python的安装目录下

谷歌驱动：[ChromeDriver - WebDriver for Chrome (google.com)](https://sites.google.com/chromium.org/driver/)

## 2. 基本使用

```python
from selenium import webdriver

option = webdriver.ChromeOptions()
#是否显示浏览器 如果想显示浏览器，请把这两行注释掉
#option.add_argument('--headless')
# option.add_argument('--disable-gpu')
# option.add_argument('--headless')
# option.add_argument('--no-sandbox')
# option.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options = option)
driver.get("http://www.baidu.com")

driver.close()
driver.quit()
```

## 3. 元素定位

```python

```

## 4. webdriver中的等待

### 4.1 强制等待:sleep()

```python
import time
sleep(5)  #等待5秒
```

### 4.2 隐式等待:implicitly_wait()

```python
'''
由webdriver提供的方法，一旦设置，这个隐式等待会在WebDriver对象实例的整个生命周期起作用，它不针对某一个元素，是全局元素等待，即在定位元素时，需要等待页面全部元素加载完成，才会执行下一个语句。如果超出了设置时间的则抛出异常。
'''
driver.implicitly_wait(10) #隐式等待10秒
```

### 4.3 显示等待:WebDriverWait()

```python
from selenium.webdriver.support.wait import WebDriverWait

'''
WebDriverWait(driver,timeout,poll_frequency=0.5,ignored_exceptions=None)

driver：浏览器驱动
timeout：最长超时时间，默认以秒为单位
poll_frequency：检测的间隔步长，默认为0.5s
ignored_exceptions：超时后的抛出的异常信息，默认抛出NoSuchElementExeception异常。
'''
```

#### 4.3.1 WebDriverWait与until一起使用

```python
'''WebDriverWait与until一起使用'''
from selenium.webdriver.support.wait import WebDriverWait

wait = WebDriverWait(driver,10)  
# 在设置时间（10s）内，等待后面的条件发生。如果超过设置时间未发生，则抛出异常。在等待期间，每隔一定时间（默认0.5秒)，调用until或until_not里的方法，直到它返回True或False.
wait.until(method，message="")
wait.until_not(method，message="")
```

#### 4.3.2 WebDriverWait与expected_conditions结合使用

```python
'''WebDriverWait与expected_conditions结合使用'''
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wait = WebDriverWait(driver,10,0.5)
element =wait.until(EC.presence_of_element_located((By.ID,"kw")),message="")
# 此处注意，如果省略message=“”，则By.ID外面是三层()
```

#### 4.3.3 自定义等待条件

```python
#设置等待
wait = WebDriverWait(driver,10,0.5)
#使用匿名函数
wait.until(lambda diver:driver.find_element_by_id('kw'))
```

