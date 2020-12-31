# baidu_ocr_test

## 采用百度接口做OCR标注

### python test_python.py 去获取百度AI通用文字识别的AK
### python baidu_ocr.py 调用百度的OCR文字识别的接口进行自己数据集的标记，里面进行了一定的后处理
### bash check_baidu_run.sh 对baidu_ocr.py的进程进行监控，当发现进程意外停止的时候，重启服务。
### image_deal.py 使用传统opencv方法对有噪声的图片进行去噪处理：
* 进行数据增强
* 去线性噪声
* 对小噪点进去去除
* 对大噪点进行去除
