from operator import mod
import torch

''' 1. 准备数据集'''
x_data = torch.Tensor([[1.0], [2.0], [3.0], [4.0]])
y_data = torch.Tensor([[2.0], [4.0], [6.0], [8.0]])


''' 2. 构造模型'''    
class LinearModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(1,1)   # torch.nnj.Linear(in_feature_size, out_feature_size, if_bias)
    
    
    def forward(self, x):
        y_pred = self.linear(x)      # self.linear中含有__call__()方法
        return y_pred


model = LinearModel()          # 创建model实例，含有__call__()方法，model(x)会自动调用forward(x)函数


''' 3. 构造损失函数和优化器'''
criterion = torch.nn.MSELoss(size_average=False)                 # 构造损失函数
optimizer = torch.optim.SGD(model.parameters(), lr = 0.01)       # 构造优化器，用于更新权重值


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
    loss = criterion(y_data, y_pred)   # 计算损失函数值
    print(epoch, loss.item())
    
    optimizer.zero_grad()        # 把所有权重的梯度归零（因为.backward()函数会累加梯度值，因此在调用.backward()函数前需要进行梯度归零）
    loss.backward()              # 反向传播
    optimizer.step()             # 更新权重值

# output weight and bias
print('w=', model.linear.weight.item())
print('b=', model.linear.bias.item())


''' 5. 测试模型'''
# test model
x_test = torch.Tensor([[5.0], [6.0]])
y_test = model(x_test)

print(y_test.data)