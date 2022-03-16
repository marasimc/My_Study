# pyautogui库的基本用法

## 常用操作

```python
import pyautogui

pyautogui.PAUSE = 1        # 调用在执行动作后暂停的秒数，只能在执行一些pyautogui动作后才能使用，建议用time.sleep
pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常

# 判断(x,y)是否在屏幕上
x, y = 122, 244
pyautogui.onScreen(x, y)         # 结果为true/False

width, height = pyautogui.size() # 获取屏幕的宽度和高度
print(width, height)
```



## 鼠标操作

```python
import pyautogui

currentMouseX, currentMouseY = pyautogui.position() # 获取鼠标当前位置
print(currentMouseX, currentMouseY)

# 控制鼠标移动,duration为持续时间
for i in range(2):
pyautogui.moveTo(100, 100, duration=0.25) # 移动到 (100,100)
pyautogui.moveTo(200, 100, duration=0.25)
pyautogui.moveTo(200, 200, duration=0.25)
pyautogui.moveTo(100, 200, duration=0.25)
for i in range(2):
pyautogui.moveRel(50, 0, duration=0.25)  # 从当前位置右移100像素
pyautogui.moveRel(0, 50, duration=0.25)  # 向下
pyautogui.moveRel(-50, 0, duration=0.25) # 向左
pyautogui.moveRel(0, -50, duration=0.25) # 向上

# 按住鼠标左键，把鼠标拖拽到(100, 200)位置
pyautogui.dragTo(100, 200, button='left')
# 按住鼠标左键，用2秒钟把鼠标拖拽到(300, 400)位置
pyautogui.dragTo(300, 400, 2, button='left')
# 按住鼠标左键，用0.2秒钟把鼠标向上拖拽
pyautogui.dragRel(0, -60, duration=0.2)

# pyautogui.click(x=moveToX, y=moveToY, clicks=num_of_clicks, interval=secs_between_clicks, button='left')
# 其中，button属性可以设置成left，middle和right。
pyautogui.click(10, 20, 2, 0.25, button='left')
pyautogui.click(x=100, y=200, duration=2) # 先移动到(100, 200)再单击
pyautogui.click()       # 鼠标当前位置点击一下
pyautogui.doubleClick() # 鼠标当前位置左击两下
pyautogui.doubleClick(x=100, y=150, button="left") # 鼠标在（100，150）位置左击两下
pyautogui.tripleClick() # 鼠标当前位置左击三下
pyautogui.mouseDown()   # 鼠标左键按下再松开
pyautogui.mouseUp()
pyautogui.mouseDown(button='right') # 按下鼠标右键
pyautogui.mouseUp(button='right', x=100, y=200) # 移动到(100, 200)位置，然后松开鼠标右键

""" scroll函数控制鼠标滚轮的滚动，amount_to_scroll参数表示滚动的格数。正数则页面向上滚动，负数则向下滚动"""
# pyautogui.scroll(clicks=amount_to_scroll, x=moveToX, y=moveToY)
pyautogui.scroll(5, 20, 2)
pyautogui.scroll(10)  # 向上滚动10格
pyautogui.scroll(-10) # 向下滚动10格
pyautogui.scroll(10, x=100, y=100) # 移动到(100, 100)位置再向上滚动10格

# 缓动/渐变函数可以改变光标移动过程的速度和方向。通常鼠标是匀速直线运动，这就是线性缓动/渐变函数。
# PyAutoGUI有30种缓动/渐变函数，可以通过pyautogui.ease*?查看。
# 开始很慢，不断加速
pyautogui.moveTo(100, 100, 2, pyautogui.easeInQuad)
# 开始很快，不断减速
pyautogui.moveTo(100, 100, 2, pyautogui.easeOutQuad)
# 开始和结束都快，中间比较慢
pyautogui.moveTo(100, 100, 2, pyautogui.easeInOutQuad)
# 一步一徘徊前进
pyautogui.moveTo(100, 100, 2, pyautogui.easeInBounce)
# 徘徊幅度更大，甚至超过起点和终点
pyautogui.moveTo(100, 100, 2, pyautogui.easeInElastic)
```

```python
"""案例获取鼠标的位置，方便复制我们定位的鼠标坐标点到代码中"""

import pyautogui
import time

# 获取鼠标位置
def get_mouse_positon():
    time.sleep(5) # 准备时间
    print('开始获取鼠标位置')
    try:
        for i in range(10):
        # Get and print the mouse coordinates.
        x, y = pyautogui.position()
        positionStr = '鼠标坐标点（X,Y）为：{},{}'.format(str(x).rjust(4), str(y).rjust(4))
        pix = pyautogui.screenshot().getpixel((x, y)) # 获取鼠标所在屏幕点的RGB颜色
        positionStr += ' RGB:(' + str(pix[0]).rjust(3) + ',' + str(pix[1]).rjust(3) + ',' + str(pix[2]).rjust(
        3) + ')'
        print(positionStr)
        time.sleep(0.5) # 停顿时间
    except:
    	print('获取鼠标位置失败')
        
if __name__ == "__main__":
	get_mouse_positon()
```

## 键盘操作

```python
import pyautogui

pyautogui.typewrite('Hello world!') # 输入Hello world!字符串
pyautogui.typewrite('Hello world!', interval=0.25) # 每次输入间隔0.25秒，输入Hello world!
pyautogui.press('enter') # 按下并松开（轻敲）回车键
pyautogui.press(['left', 'left', 'left', 'left']) # 按下并松开（轻敲）四下左方向键
pyautogui.keyDown('shift') # 按下`shift`键
pyautogui.keyUp('shift') # 松开`shift`键
pyautogui.keyDown('shift')
pyautogui.press('4')
pyautogui.keyUp('shift') # 输出 $ 符号的按键
pyautogui.hotkey('ctrl', 'v') # 组合按键（Ctrl+V），粘贴功能，按下并松开'ctrl'和'v'按键
# pyautogui.KEYBOARD_KEYS数组中就是press()，keyDown()，keyUp()和hotkey()函数可以输入的按键名称
pyautogui.KEYBOARD_KEYS = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',
'/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', ' ', '?', '@',
'[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback',
'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch',
'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal',
'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22',
'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul',
'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2',
'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9',
'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print',
'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select',
'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command',
'option', 'optionleft', 'optionright']
```

## 弹窗操作

```python
import pyautogui

# 显示一个简单的带文字和OK按钮的消息弹窗。用户点击后返回button的文字。
pyautogui.alert(text='', title='', button='OK')
b = pyautogui.alert(text='要开始程序么？', title='请求框', button='OK')
print(b) # 输出结果为OK

# 显示一个简单的带文字、OK和Cancel按钮的消息弹窗，用户点击后返回被点击button的文字，支持自定义数字、文字的列表。
pyautogui.confirm(text='', title='', buttons=['OK', 'Cancel']) # OK和Cancel按钮的消息弹窗
pyautogui.confirm(text='', title='', buttons=range(10)) # 10个按键0-9的消息弹窗
a = pyautogui.confirm(text='', title='', buttons=range(10))
print(a) # 输出结果为你选的数字

# 可以输入的消息弹窗，带OK和Cancel按钮。用户点击OK按钮返回输入的文字，点击Cancel按钮返回None。
pyautogui.prompt(text='', title='', default='')
# 样式同prompt()，用于输入密码，消息用*表示。带OK和Cancel按钮。用户点击OK按钮返回输入的文字，点击Cancel按钮返回None。
pyautogui.password(text='', title='', default='', mask='*')
```

## 图像操作

```python
import pyautogui

pyautogui.screenshot(r'my_screenshot.png')       # 截全屏并设置保存图片的位置和名称
im = pyautogui.screenshot(r'my_screenshot.png')  # 截全屏并设置保存图片的位置和名称
print(im) # 打印图片的属性

# 不截全屏，截取区域图片。截取区域region参数为：左上角XY坐标值、宽度和高度
pyautogui.screenshot(r'region_screenshot.png', region=(0, 0, 300, 400))

pix = pyautogui.screenshot().getpixel((220, 200)) # 获取坐标(220,200)所在屏幕点的RGB颜色
positionStr = ' RGB:(' + str(pix[0]).rjust(3) + ',' + str(pix[1]).rjust(3) + ',' + str(pix[2]).rjust(3) + ')'
print(positionStr) # 打印结果为RGB:( 60, 63, 65)

pix = pyautogui.pixel(220, 200)  # 获取坐标(220,200)所在屏幕点的RGB颜色与上面三行代码作用一样
positionStr = ' RGB:(' + str(pix[0]).rjust(3) + ',' + str(pix[1]).rjust(3) + ',' + str(pix[2]).rjust(3) + ')'
print(positionStr) # 打印结果为RGB:( 60, 63, 65)

# 如果你只是要检验一下指定位置的像素值，可以用pixelMatchesColor(x,y,RGB)函数，把X、Y和RGB元组值穿入即可
# 如果所在屏幕中(x,y)点的实际RGB三色与函数中的RGB一样就会返回True，否则返回False
# tolerance参数可以指定红、绿、蓝3种颜色误差范围
pyautogui.pixelMatchesColor(100, 200, (255, 255, 255))
pyautogui.pixelMatchesColor(100, 200, (255, 255, 245), tolerance=10)

# 获得文件图片在现在的屏幕上面的坐标，返回的是一个元组(top, left, width, height)
# 如果截图没找到，pyautogui.locateOnScreen()函数返回None
a = pyautogui.locateOnScreen(r'C:\Users\ZDH\Desktop\PY\region_screenshot.png')
print(a)    # 打印结果为Box(left=0, top=0, width=300, height=400)
x, y = pyautogui.center(a) # 获得文件图片在现在的屏幕上面的中心坐标
print(x, y) # 打印结果为150 200
x, y = pyautogui.locateCenterOnScreen(r'C:\Users\ZDH\Desktop\PY\region_screenshot.png') # 这步与上面的四行代码作用一样
print(x, y) # 打印结果为150 200

# 匹配屏幕所有与目标图片的对象，可以用for循环和list()输出
pyautogui.locateAllOnScreen(r'region_screenshot.png')
for pos in pyautogui.locateAllOnScreen(r'region_screenshot.png'):
	print(pos)
# 打印结果为Box(left=0, top=0, width=300, height=400)
a = list(pyautogui.locateAllOnScreen(r'region_screenshot.png'))
print(a) # 打印结果为[Box(left=0, top=0, width=300, height=400)]
```

