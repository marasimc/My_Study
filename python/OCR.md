# OCR工具

## cnocr  -- 中文

```python
from cnocr import CnOcr

ocr = CnOcr()
res = ocr.ocr('test1.png')
print("Predicted Chars:", res)
```



## paddleocr  

```python
import paddlehub as hub 
import cv2 
ocr = hub.Module(name="chinese_ocr_db_crnn_server") 
result = ocr.recognize_text(images=[cv2.imread('test1.png')])
# or # result = ocr.recognize_texts(paths=['/PATH/TO/IMAGE'])
print(result)
```



## easyocr

```python
import easyocr
# 创建reader对象
reader = easyocr.Reader(['ch_sim', 'en']) 
# 读取图像
result = reader.readtext('test1.png')
# 结果
print(list(result))
```



## Chineseocr-lite

https://github.com/DayBreak-u/chineseocr_lite
