from pyexpat import model
import torch
from torch.utils.data import Dataset     # 抽象类 本不可以直接进行实例化
from torch.utils.data import DataLoader
import numpy as np


""" 1. 准备数据集 """
class DiabatesDataset(Dataset):
    def __init__(self, filepath):
        xy = np.loadtxt(filepath, delimiter=',', dtype=np.float32)
        self.len = xy.shape[0]
        self.x_data = torch.from_numpy(xy[:,:-1])
        self.y_data = torch.from_numpy(xy[:,[-1]])
    
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
        
    
    def __len__(self):
        return self.len

filepath = 'dataset/diabetes.csv'
dateset = DiabatesDataset(filepath)

train_loader = DataLoader(dataset=dateset, 
                          batch_size=32,
                          shuffle=True,
                          num_workers=2         # 读取数据时并行的进程数
                          )


""" 2. 构造模型 """
class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = torch.nn.Linear(8,6)
        self.linear2 = torch.nn.Linear(6,4)
        self.linear3 = torch.nn.Linear(4,1)
        self.sigmoid = torch.nn.Sigmoid()
    
    def forward(self, x):
        x = self.sigmoid(self.linear1(x))
        x = self.sigmoid(self.linear2(x))
        x = self.sigmoid(self.linear3(x))
        return x

model = Model()


""" 3. 构造损失函数和优化器 """
criterion = torch.nn.BCELoss(size_average=False)
optimizer = torch.optim.SGD(model.parameters(), lr = 0.1)


""" 4. 模型训练 Mini-Batch"""
def train():
    for epoch in range(10):
        for i, data in enumerate(train_loader, 0):
            # 1. prepare data
            inputs, labels = data    # inputs, labels 都是张量
            
            # 2. forward
            y_pred = model(inputs)
            loss = criterion(y_pred, labels)
            
            print(epoch, i, loss.item())
            
            # 3. backward
            optimizer.zero_grad()
            loss.backward()
            
            # 4. update
            optimizer.step()


if __name__ == '__main__':
    train()

    # test model
    x_test = np.loadtxt('dataset/diabetes_test.csv', delimiter=',', dtype=np.float32)
    x_test = torch.from_numpy(x_test[:,:-1])
    y_test = model(x_test)

    print(y_test.data)