import torch


def test_RNNCell():
    '''
        测试torch.nn.RNNCell用法
    '''
    batch_size = 1
    seq_len  =3
    input_size = 4
    hidden_size = 2

    cell = torch.nn.RNNCell(input_size=input_size, hidden_size=hidden_size)

    dataset = torch.randn(seq_len, batch_size, input_size)
    hidden = torch.zeros(batch_size, hidden_size)           # 初始h0设置为全0

    for idx, input in enumerate(dataset):
        print('='*20, idx, '='*20)
        print('input_size:', input.shape)
        
        hidden = cell(input, hidden)
        
        print('output_size:', hidden.shape)
        print(hidden)


def test_RNN():
    '''
        测试torch.nn.RNN用法
    '''
    batch_size = 1
    seq_len  =3
    input_size = 4
    hidden_size = 2
    num_layers = 1
    
    cell = torch.nn.RNN(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers)
    
    dataset = torch.randn(seq_len, batch_size, input_size)
    hidden = torch.zeros(num_layers, batch_size, hidden_size)           # 初始h0设置为全0
    
    out, hidden = cell(dataset, hidden)
    
    print('output_size:', out.shape)
    print('out:', out)
    print('hidden_size:', hidden.shape)
    print('hidden:', hidden)



if __name__=='__main__':
    test_RNN()