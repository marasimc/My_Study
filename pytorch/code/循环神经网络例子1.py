'''
    使用RNNCell
'''
import torch

input_size = 4
hidden_size = 4
batch_size = 1

idx2char = ['e', 'h', 'l', 'o']
# 有 hello 学习 ohlol
x_data = [1,0,2,2,3]    # 表示 hello
y_data = [3,1,2,3,2]    # 表示 ohlol

one_hot_lookup = [[1,0,0,0],
                  [0,1,0,0],
                  [0,0,1,0],
                  [0,0,0,1]]
x_one_hot = [one_hot_lookup[x] for x in x_data]   # 构造独热向量

inputs = torch.Tensor(x_one_hot).view(-1, batch_size, input_size)
labels = torch.LongTensor(y_data).view(-1, 1)
# print(labels)

class Model(torch.nn.Module):
    def __init__(self, input_size, hidden_size, batch_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.rnncell = torch.nn.RNNCell(input_size=self.input_size, hidden_size=self.hidden_size)
    
    def forward(self, input, hidden):
        hidden = self.rnncell(input, hidden)
        return hidden
    
    def init_hidden(self):
        return torch.zeros(self.batch_size, self.hidden_size)

net = Model(input_size, hidden_size, batch_size)


criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr=0.1)

def train():
    '''
        模型训练
    '''
    for epoch in range(15):
        loss = 0
        
        hidden = net.init_hidden()
        print('predicted string:', end='')
        
        for input, label in zip(inputs, labels):
            hidden = net(input, hidden)
            # print(hidden)
            
            loss += criterion(hidden, label)     # 注意这里累加时不取item，因为需要构造计算图
            _, idx = hidden.max(dim=1)
            print(idx2char[idx.item()], end='')
            
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
            
        print(', Epoch[%d/15] loss = %.4f' % (epoch+1, loss.item()))

train()