# Tensorboard用法

## 1. SummaryWriter()

```python
from tensorboardX import SummaryWriter

writer = SummaryWriter(log_dir='logs',flush_secs=60)
# log_dir：tensorboard文件的存放路径
# flush_secs：表示写入tensorboard文件的时间间隔
```

## 2. writer.add_graph()

```python
'''
这个函数用于在tensorboard中创建Graphs，Graphs中存放了网络结构，其中常用参数有：

model：pytorch模型
input_to_model：pytorch模型的输入
'''

if Cuda:
    graph_inputs = torch.from_numpy(np.random.rand(1,3,input_shape[0],input_shape[1])).type(torch.FloatTensor).cuda()
else:
    graph_inputs = torch.from_numpy(np.random.rand(1,3,input_shape[0],input_shape[1])).type(torch.FloatTensor)
    
writer.add_graph(model, (graph_inputs,))
```

## 3. writer.add_scalar()

```python
'''
这个函数用于在tensorboard中加入loss，其中常用参数有：
tag：标签，如下图所示的Train_loss
scalar_value：标签的值
global_step：标签的x轴坐标
'''

# 训练的循环中，每次写入 图像名称，loss数值， n_iteration
writer.add_scalar('Train/Loss', loss.data[0], niter)

# 验证的循环中，写入预测的准确度即可
writer.add_scalar('Test/Accu', correct/total, niter)
```

## 4. tensorboard --logdir=

```python
'''
在完成tensorboard文件的生成后，可在命令行调用该文件，tensorboard网址。
'''
''' 显示 '''
终端输入： tensorboard --logdir=./log
浏览器访问：http://0.0.0.0:6006/
```

