# import torch

# in_channels, out_channels= 5, 10
# width, height = 5, 5
# kernel_size = 3
# batch_size = 1
# input = torch.randn(batch_size,
#                     in_channels,
#                     width, 
#                     height)
# print(input)

class test():
    def get(self):
        print('1')

t = test()
t.get()

del t

t.get()