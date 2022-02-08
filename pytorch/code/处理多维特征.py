'''
    以皮马人糖尿病预测数据集为例进行测试
    来源
 https://www.kaggle.com/uciml/pima-indians-diabetes-database#diabetes.csv
 https://github.com/susanli2016/Machine-Learning-with-Python/blob/master/diabetes.csv
'''
import numpy as np
import torch

# x = np.loadtxt('dataset/diabetes_data.csv.gz', delimiter=' ', dtype=np.float32)
# y = np.loadtxt('dataset/diabetes_target.csv.gz', delimiter=' ', dtype=np.float32)
# print(y[:10])
# x_data = torch.from_numpy(x)
# y_data = torch.from_numpy(y)
# size = y_data.shape[0]
# y_data = y_data.view(size, 1)
# print(y_data[:10])

xy = np.loadtxt('dataset/diabetes.csv', delimiter=',', dtype=np.float32)
x_data = torch.from_numpy(xy[:,:-1])
y_data = torch.from_numpy(xy[:,[-1]])


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


criterion = torch.nn.BCELoss(size_average=False)               # BCELoss: binary CrossEntropyLoss,二分类交叉熵损失函数，用于输出层为sigmoid()激活函数时（二分类问题和多标签分类问题）
optimizer = torch.optim.SGD(model.parameters(), lr = 0.1)     # 构造优化器，用于更新权重值


for epoch in range(10):
    y_pred = model(x_data)             
    loss = criterion(y_pred, y_data)   # 计算损失函数值, 必须把y_pred写在前, y_data写在后
    # loss = criterion(y_data, y_pred)   # 计算损失函数值
    print(epoch, loss.item())
    
    optimizer.zero_grad()        # 把所有权重的梯度归零（因为.backward()函数会累加梯度值，因此在调用.backward()函数前需要进行梯度归零）
    loss.backward()              # 反向传播
    
    optimizer.step()             # 更新权重值


# test model
x_test = np.loadtxt('dataset/diabetes_test.csv', delimiter=',', dtype=np.float32)
x_test = torch.from_numpy(x_test[:,:-1])
y_test = model(x_test)

print(y_test.data)