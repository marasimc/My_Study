# 1. 截图

```python
'''实现屏幕截图'''
import win32gui, win32ui, win32con, win32api, win32com
import time

def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        # 返回坐标值和handle
        return win32gui.GetWindowRect(handle), handle
    

def window_capture(hwnd, filename):
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)


if __name__ == '__main__':

    hWnd_location, hWnd = get_window_pos('同花顺(v8.90.91) - 1号方案')   ## '同花顺(v8.90.91) - 1号方案'为待获取句柄的名字

    print(hWnd_location)
	#将程序界面置顶
    win32gui.SendMessage(hWnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)  # 这句很重要，这句可以保证将句柄置到前端
    win32gui.SetForegroundWindow(hWnd)

    time.sleep(1)
    window_capture(hWnd, "1.png")
```

# 2. 获取所有句柄及窗口名称

```python
'''获取所有句柄及窗口名称''' 
import win32gui

hwnd_title = dict()

def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
win32gui.EnumWindows(get_all_hwnd, 0)
 
for h,t in hwnd_title.items():
    if t is not "":
        print(h, t)
```

# 3. **根据进程标题名称隐藏运行进程**

```python
import win32gui
 
from win32.lib import win32con
 
 
 
def handle_window(hwnd, extra):
	if win32gui.IsWindowVisible(hwnd):
 
		if '需要隐藏的程序标题名称' in win32gui.GetWindowText(hwnd):
			win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
 
 
if __name__ == '__main__':
	win32gui.EnumWindows(handle_window, None)
 
 
# win32gui.EnumWindows(枚举函数名称, None) 语句是进行句柄ID枚举 
# win32gui.GetWindowText(句柄ID) 语句是通过句柄ID来获取进程名称
# win32gui.IsWindowVisible(句柄ID) 语句是查询此句柄ID是否存在，存在返回1 否则返回0
# win32gui.ShowWindow(句柄ID, win32con.SW_HIDE) 语句是通过指定句柄ID来隐藏进程
```

# 4. **根据程序名称来获取进程PID，然后通过PID杀掉进程**

```python
import win32gui
import win32process
import psutil
 
 
 
def handle_window(hwnd, extra):
	if win32gui.IsWindowVisible(hwnd):
 
		if '程序标题' in win32gui.GetWindowText(hwnd):               # 判断是否符合
			_,PID = win32process.GetWindowThreadProcessId(hwnd)     # 通过句柄ID查询进程PID（第0个元素不管，第1个元素是PID）
			p = psutil.Process(PID)                                 # 实例化PID
			p.terminate()                                           # 关闭PID进程
 
 
if __name__ in "__main__":
    win32gui.EnumWindows(handle_window, None)                           # 通过句柄ID查询PID并关闭PID
```

# 5. **根据PID查询，返回句柄ID**

```python
import win32gui
import win32process
 
def get_hwnds_for_pid(pid):
	# 通过PID查询句柄ID
	def callback(hwnd, hwnds):
		if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
			_, found_pid = win32process.GetWindowThreadProcessId(hwnd)
			if found_pid == pid:
				hwnds.append(hwnd)
			return True
 
	hwnds = []
	win32gui.EnumWindows(callback, hwnds)
	hwndy = 0
	if hwnds:
		hwndy = hwnds[0]
 
	return hwndy
 
 
if __name__ in "__main__":
    get_hwnds_for_pid(传入PID值)  # 传入PID值后返回句柄ID
```

