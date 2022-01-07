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
    

def window_capture(filename):
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
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
    window_capture("1.png")
```

