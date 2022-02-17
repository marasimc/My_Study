import torch

def CNN_test():
    '''
        测试图像基本卷积操作
    '''
    in_channels, out_channels = 5, 10       # 输入通道数，输出通道数
    width, height = 100, 100                # 输入图像的宽度、高度
    kernel_size = 3
    batch_size = 2

    input = torch.randn(batch_size, 
                        in_channels,
                        width,
                        height)

    conv_layer = torch.nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size)

    output = conv_layer(input)

    print(input.shape)                # torch.Size([2, 5, 100, 100]) -> 5X100X100
    print(output.shape)               # torch.Size([2, 10, 98, 98]) -> 10X98X98   (因为卷积核为3X3大小，因此图像大小减2)
    print(conv_layer.weight.shape)    # 输出卷积核的维度  torch.Size([10, 5, 3, 3]) 


def padding_test():
    '''
        测试convolutional layer 的 padding 操作
    '''
    input = [3,4,6,5,7,
             2,4,6,8,2,
             1,6,7,8,4,
             9,7,4,6,2,
             3,7,5,4,1]
    input = torch.Tensor(input).view(1,1,5,5)  # batch_size X channel X width X height
    
    conv_layer = torch.nn.Conv2d(1,1,kernel_size=3,padding=1, bias=False)  # bias=False 表示在进行卷积之后不需要为每一个通道加偏置量
    
    kernel = torch.Tensor([1,2,3,4,5,6,7,8,9]).view(1,1,3,3)  # 构造卷积核
    conv_layer.weight.data = kernel.data                      # 设置卷积层的卷积核的值
    
    output = conv_layer(input)
    print(output)


def max_pooling_test():
    '''
        测试Max_pooling(最大池化)
    '''
    input = [3,4,6,5,7,
             2,4,6,8,2,
             1,6,7,8,4,
             9,7,4,6,2,
             3,7,5,4,1]
    input = torch.Tensor(input).view(1,1,5,5)  # batch_size X channel X width X height
    
    max_pooling_layer = torch.nn.MaxPool2d(kernel_size=2)   # 默认的步长为2， 即stride = 2
    
    output = max_pooling_layer(input)
    print(output)
    

if __name__=='__main__':
    padding_test()