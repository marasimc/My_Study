# 1. 比较两张图片

```python
import cv2
import numpy as np
#import os
 

def is_same(img1, img22):
    image1 = cv2.imread(img1)
    image2 = cv2.imread(img22)
    difference_1 = cv2.subtract(image1, image2)
    difference_2 = cv2.subtract(image2, image1)
    # print(difference)
    result = not np.any(difference_1) #if difference is all zeros it will return False
    if result:
        result = not np.any(difference_2) #if difference is all zeros it will return False
    
    if result is True:
        print("两张图片一样")
    else:
        cv2.imwrite("result.jpg", difference)
        print ("两张图片不一样")

if __name__=='__main__':
    file1= "1.png"
    file2="2.png"
    
    is_same(file1, file2)
```

