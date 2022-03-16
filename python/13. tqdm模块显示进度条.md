# tqdm模块显示进度条

```python
from tqdm import tqdm
import time, random

all_list = [1,2,3,4,5,6,7,8]

with tqdm(total=100) as p_bar:
    for item in all_list:
        time.sleep(random.random())
        p_bar.update(100/(len(all_list)))
        p_bar.set_description("Processing {}-th iteration".format(i+1))
```

