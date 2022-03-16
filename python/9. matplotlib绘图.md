python绘图：

```python
'''
    根据真实值和预测值进行绘制曲线图反映预测的程度
'''
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.pylab as pyl
import numpy as np
from scipy.interpolate import make_interp_spline

plt.rcParams['font.sans-serif'] = ['SimHei']  #SimHei黑体  FangSong仿宋
plt.rcParams['axes.unicode_minus'] = False


def Draw_predict_data(x_arr, y1_arr, y2_arr, title, y_lable):
    '''
        input:  y1_arr为真实值， y2_arr为预测值； x_arr为时间点
                title: 标题； y_label: y标签名
        output: 同一张图上的两条折线
    '''
    plt.figure()
    plt.plot(x_arr, y1_arr, label="真实值", linestyle=":")
    plt.plot(x_arr, y2_arr, label="预测值", linestyle="--")

    plt.legend()
    plt.title(title)
    plt.xlabel("时间")
    plt.ylabel(y_lable)
    plt.show()


def Draw_status_data(x_arr, y1_arr, y2_arr, title, y_label):
    '''
        input:
        output: 同一张图下的两个散点图(用于表示涨跌转态)
    '''
    x_com = [];   y_com = []   # 表示两个的共同点
    for i in range(len(x_arr)):
        if y1_arr[i]==y2_arr[i]:
            x_com.append(x_arr[i])
            y_com.append(y1_arr[i])

    plt.figure()
    plt.scatter(x_arr, y1_arr, s=4, c='red', label='真实值')
    plt.scatter(x_arr, y2_arr, s=4, c='black', label='预测值')
    plt.scatter(x_com, y_com, s=4, c='green', label='共同值')
    plt.legend()
    plt.title(title)
    plt.xlabel("时间")
    plt.ylabel(y_label)
    plt.show()


def Draw_min_max_data(x_all, y_all, x_max_min, y_max_min, label):
    '''
        input:
        output: 同一张图下的一条折线 + 两个散点图（min max）
    '''
    plt.figure()
    plt.plot(x_all, y_all, label="真实值", linestyle="--")
    plt.scatter(x_max_min, y_max_min, s=4, c='green', label=label)
    plt.legend()
    plt.title('最大最小涨跌幅度预测')
    plt.xlabel("时间")
    plt.ylabel('ic值')
    plt.show()
```

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']    #SimHei黑体  FangSong仿宋
plt.rcParams['axes.unicode_minus'] = False


def draw(x_arr, y1_arr, y2_arr, success_pos):
    '''
        绘图
        @param:  x_arr -> x坐标
                 y1_arr -> 历史3-6个月的收盘价
                 y2_arr -> 选中的那点后30天的最高价
                 success_pos ->
        @return:
    '''
    x_pos = [x_arr[i] for i in success_pos]
    y1_pos = [y1_arr[i] for i in success_pos]
    y2_pos = [y2_arr[i] for i in success_pos]

    plt.figure()
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))   # 设置x轴间隔多少个数据进行显示
    plt.plot(x_arr, y1_arr, label="当天收盘价", linestyle=":")
    plt.plot(x_arr, y2_arr, label="30天后的最高价", linestyle="--")
    plt.scatter(x_pos, y1_pos, s=10, c='green', label='满足成功条件的当天收盘价')
    plt.scatter(x_pos, y2_pos, s=10, c='red', label='满足成功条件的30天后的最高价')

    plt.legend()
    plt.title('历史3-6个月的成功率测试曲线')
    plt.xlabel("时间")
    plt.ylabel('值')
    plt.show()
```

## 为点绘制平滑曲线

```python
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline

x = np.array([6, 7, 8, 9, 10, 11, 12])
y = np.array([1.53E+03, 5.92E+02, 2.04E+02, 7.24E+01, 2.72E+01, 1.10E+01, 4.70E+00])
x_smooth = np.linspace(x.min(), x.max(), 300)
y_smooth = make_interp_spline(x, y)(x_smooth)
plt.plot(x_smooth, y_smooth)
plt.show()
```

