# OCR工具

## cnocr

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

