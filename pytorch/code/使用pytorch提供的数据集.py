import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision import datasets


### 手写数字识别数据集
train_dataset = datasets.MNIST(root='D:/data/dataset/pytorch/mnist',  # 存放的路径
                               train=True,                            # 是否为训练集
                               transform=transforms.ToTensor(),       # 读取的数据为以pillow方式存储的数据，需要转换成tensor
                               download=True)

test_dataset = datasets.MNIST(root='D:/data/dataset/pytorch/mnist',
                              train=False,
                              transform=transforms.ToTensor(),
                              download=True)

train_loader = DataLoader(dataset=train_dataset, 
                          batch_size=32,
                          shuffle=True)          # 训练数据集一般需要打乱顺序
test_loader = DataLoader(dataset=test_dataset,
                         batch_size=32,
                         shuffle=False)          # 测试数据集一般不进行打乱顺序，有利于观察结果