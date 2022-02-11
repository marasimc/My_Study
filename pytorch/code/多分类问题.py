import torch
import numpy as np
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torch.optim as optim


def cross_entropy_test():
    '''
        测试交叉熵损失函数,torch.nn.CrossEntropyLoss() 此函数包含有softmax操作，因此传入其中的数据不需要做激活操作(非线性变换)
    '''
    criterion = torch.nn.CrossEntropyLoss()
    
    Y = torch.LongTensor([2,0,1])
    
    Y_pred1 = torch.Tensor([[0.1, 0.2, 0.9],
                            [0.5, 0.3, 0.1],
                            [0.8, 0.7, 0.3]])
    Y_pred2 = torch.Tensor([[0.8, 0.2, 0.3],
                            [0.2, 0.3, 0.5],
                            [0.2, 0.2, 0.5]])
    
    loss1 = criterion(Y_pred1, Y)
    loss2 = criterion(Y_pred2, Y)
    print('loss1:', loss1)
    print('loss2:', loss2)
    
    

batchsize = 64
# 神经网络的输入最好在0-1之间，符合正态分布，这样效果最好
transform = transforms.Compose([
    transforms.ToTensor(),                          # convert the PIL image to Tensor
    transforms.Normalize((0.1307, ), (0.3081, ))    # 数据标准化(均值，标准差)，根据整个MNIST数据集样本计算出来的结果
])


### 手写数字识别数据集
train_dataset = datasets.MNIST(root='D:/data/dataset/pytorch/mnist',  # 存放的路径
                               train=True,                            # 是否为训练集
                               transform=transform,                   # 读取的数据为以pillow方式存储的数据，需要转换成tensor
                               download=True)

test_dataset = datasets.MNIST(root='D:/data/dataset/pytorch/mnist',
                              train=False,
                              transform=transform,
                              download=True)

train_loader = DataLoader(dataset=train_dataset, 
                          batch_size=32,
                          shuffle=True)          # 训练数据集一般需要打乱顺序
test_loader = DataLoader(dataset=test_dataset,
                         batch_size=32,
                         shuffle=False)          # 测试数据集一般不进行打乱顺序，有利于观察结果


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.l1 = torch.nn.Linear(784, 512)
        self.l2 = torch.nn.Linear(512, 256)
        self.l3 = torch.nn.Linear(256, 128)
        self.l4 = torch.nn.Linear(128, 64)
        self.l5 = torch.nn.Linear(64, 10)
    
    def forward(self, x):
        x = x.view(-1, 784)
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = F.relu(self.l3(x))
        x = F.relu(self.l4(x))
        
        return self.l5(x)    # 最后一层不需要做激活操作，因为交叉熵损失函数,torch.nn.CrossEntropyLoss()含有激活操作
        
model = Net()

criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)   #由于网络较大，因此选用带冲量的优化器，设置冲量momentum = 0.5

def train(epoch):
    '''
        模型一轮训练
    '''
    running_loss = 0.0
    for batch_idx, data in enumerate(train_loader, 0):
        inputs, labels = data
        
        y_pred = model(inputs)
        loss = criterion(y_pred, labels)
        
        optimizer.zero_grad()
        loss.backward()
        
        optimizer.step()
        
        running_loss += loss.item()
        if batch_idx%300 == 299:
            print('[%d, %5d] loss: %.3f' % (epoch+1, batch_idx+1, running_loss/300))
            running_loss = 0.0


def test():
    '''
     模型测试，不需要进行反向传播,不需要计算梯度
    '''
    correct = 0
    total = 0
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            outputs = model(images)
            _, predicted = torch.max(outputs.data, dim=1)    # 取outputs中第一个维度(横向)中每一行的最大值，返回：(下标，值)
            total+=labels.size(0)                            # labels 为NX1的矩阵
            correct+=(predicted==labels).sum().item()
    
    print('accuracy on test_set: %d %%' % (100*correct/total))


if __name__ == '__main__':
    # cross_entropy_test()
    for epoch in range(10):
        train(epoch)
        test()