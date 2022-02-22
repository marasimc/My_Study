'''
    使用RNN
'''
import torch

input_size = 4
hidden_size = 4
batch_size = 1
num_layers = 1

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
labels = torch.LongTensor(y_data)


class Model(torch.nn.Module):
    def __init__(self, input_size, hidden_size, batch_size, num_layers = 1):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.num_layers = num_layers
        self.rnn = torch.nn.RNN(input_size=self.input_size, hidden_size=self.hidden_size, num_layers=self.num_layers)
    
    def forward(self, inputs):
        hidden = torch.zeros(self.num_layers, self.batch_size, self.hidden_size)   # 构造隐层h0
        out, _ = self.rnn(inputs, hidden)
        return out.view(-1, self.hidden_size)  # reshape to (seqlen X batchSize, hidden_size)
    

net = Model(input_size, hidden_size, batch_size, num_layers)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr=0.1)

def train():
    '''
        模型训练
    '''
    for epoch in range(15):
        out = net(inputs)
        loss = criterion(out, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        _, idx = out.max(dim=1)
        idx = idx.data.numpy()
        print('predicted string:',''.join([idx2char[x] for x in idx]), end='')
        print(', Epoch[%d/15] loss = %.4f' % (epoch+1, loss.item()))

train()