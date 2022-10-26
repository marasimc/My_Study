'''
    使用RNN,数据采用embedding表示，并添加线性层
'''
import torch

input_size = 4
hidden_size = 8
batch_size = 1
num_layers = 2
num_class = 4
embedding_size = 10

idx2char = ['e', 'h', 'l', 'o']
# 有 hello 学习 ohlol
x_data = [[1,0,2,2,3]]    # 表示 hello
y_data = [3,1,2,3,2]    # 表示 ohlol

# one_hot_lookup = [[1,0,0,0],
#                   [0,1,0,0],
#                   [0,0,1,0],
#                   [0,0,0,1]]
# x_one_hot = [one_hot_lookup[x] for x in x_data]   # 构造独热向量

# inputs = torch.Tensor(x_one_hot).view(-1, batch_size, input_size)
inputs = torch.LongTensor(x_data)
labels = torch.LongTensor(y_data)

print(inputs)
input = torch.unsqueeze(inputs,dim=1)  
print(input, input.shape)

class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.emb = torch.nn.Embedding(input_size, embedding_size)
        
        self.rnn = torch.nn.RNN(input_size=embedding_size, hidden_size=hidden_size, num_layers=num_layers, batch_first = True)
        self.fc = torch.nn.Linear(hidden_size, num_class)
    
    def forward(self, x):
        hidden = torch.zeros(num_layers, x.size(0), hidden_size)   # 构造隐层h0
        print(x.shape)
        x = self.emb(x)
        print(x.shape)
        x, _ = self.rnn(x, hidden)
        print(x.shape)
        x = self.fc(x)
        print(x.shape)
        print(x.view(-1, num_class).shape)
        return x.view(-1, num_class)  # reshape to (seqlen X batchSize, hidden_size)
    

net = Model()

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

# train()

net(inputs)