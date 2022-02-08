"""
    逻辑斯蒂回归测试
    处理分类问题
"""
import torch
import torch.nn.functional as F

''' 1. 准备数据集'''
x_data = torch.Tensor([[1.0], [2.0], [3.0]])
y_data = torch.Tensor([[0], [0], [1]])


''' 2. 构造模型'''   
class LogisticRegressionModel(torch.nn.Module):
    def __init__(self):
        super(LogisticRegressionModel, self).__init__()
        self.linear = torch.nn.Linear(1,1)
        
    def forward(self, x):
        y_pred = F.sigmoid(self.linear(x))   # F.sigmoid()函数用来保证值在0-1之间(1/(1+e^-x))
        return y_pred

model = LogisticRegressionModel()


''' 3. 构造损失函数和优化器'''
criterion = torch.nn.BCELoss(size_average=False)               # BCELoss: binary CrossEntropyLoss,二分类交叉熵损失函数，用于输出层为sigmoid()激活函数时（二分类问题和多标签分类问题）
optimizer = torch.optim.SGD(model.parameters(), lr = 0.01)     # 构造优化器，用于更新权重值


''' 4. 进行模型训练'''
'''
模型训练的步骤：
① 计算y_pred
② 计算loss
③ 进行反向传播(loss.backward()),注意在进行方向传播前需要进行梯度清零
④ 更新权重值
'''
for epoch in range(10):
    y_pred = model(x_data)             
    loss = criterion(y_pred, y_data)   # 计算损失函数值, 必须把y_pred写在前, y_data写在后
    # loss = criterion(y_data, y_pred)   # 计算损失函数值
    print(epoch, loss.item())
    
    optimizer.zero_grad()        # 把所有权重的梯度归零（因为.backward()函数会累加梯度值，因此在调用.backward()函数前需要进行梯度归零）
    loss.backward()              # 反向传播
    optimizer.step()             # 更新权重值

# output weight and bias
print('w=', model.linear.weight.item())
print('b=', model.linear.bias.item())


''' 5. 测试模型'''
# test model
# x_test = torch.Tensor([[5.0], [6.0]])
# y_test = model(x_test)

# print(y_test.data)

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 200)
x_test = torch.Tensor(x).view((200,1))
y_test = model(x_test)
y = y_test.data.numpy()

plt.plot(x, y)
plt.plot([0,10], [0.5,0.5], c='r')
plt.xlabel('x')
plt.ylabel('probability')
plt.grid()
plt.show()