import torch

w = torch.Tensor([1.0])
w.requires_grad = True

def forward(x):
    return w*x;

def loss(x, y):
    '''
        计算损失函数值
    '''
    return (w*x - y)**2;

def train(x, y):
    '''
        训练模型
    '''
    for epoch in range(10):
        for x,y in zip(x_data, y_data):
            l = loss(x,y)        # l 为张量
            l.backward()         # 计算梯度，并释放计算图
            
            print('grad:', x,y,w.grad.item())    # w.grad.item()取得标量值
            
            w.data = w.data - 0.01*w.grad.data   # 注意用w.grad.data去更新权重值
            w.grad.data.zero_()                  # 把由.backward()计算的权重的梯度中的数据清零，因为.backward()计算梯度时会累积
        
        print('progress:', epoch, l.item())

def predict(x):
    return forward(x).item()


if __name__ == '__main__':
    x_data = [1.0, 2.0, 3.0, 4.0]
    y_data = [2.0, 4.0, 6.0, 8.0]
    
    train(x_data, y_data)
    pred = predict(5)
    print('predict 5:', pred)