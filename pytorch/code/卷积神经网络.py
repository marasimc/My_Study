import torch
import numpy as np
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torch.optim as optim


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
        super().__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        self.pooling = torch.nn.MaxPool2d(kernel_size=2)
        self.fc = torch.nn.Linear(320,10)
    
    def forward(self, x):
        batch_size = x.size(0)         # 取样本数量（x = batch_size, channel, width, height）
        x = F.relu(self.pooling(self.conv1(x)))
        x = F.relu(self.pooling(self.conv2(x)))
        x = x.view(batch_size, -1)     # 把输入变成全连接网络需要的输入，即：(batch_size, channel, width, height) -> (batch_size, n)
        x = self.fc(x)                 # 因为要计算交叉熵损失，所以最后一层不作激活操作
        
        return x

model = Net()

# 设置使用gpu版本
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model.to(device)


criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)   #由于网络较大，因此选用带冲量的优化器，设置冲量momentum = 0.5

def train(epoch):
    '''
        模型一轮训练
    '''
    running_loss = 0.0
    for batch_idx, data in enumerate(train_loader, 0):
        inputs, labels = data
        # 把数据迁移到显卡上
        inputs, labels = inputs.to(device), labels.to(device)
        
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
            # 把数据放到显卡上
            images, labels = images.to(device), labels.to(device)
            
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