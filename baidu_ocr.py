import requests
import base64
import os
import time
import random
import json
from PIL import Image
from datetime import date, timedelta
from requests.exceptions import RequestException
file_name = (date.today() + timedelta(-1)).strftime("%Y%m%d")[-4:]
path = os.path.join(file_name + 'err/')
result_path = os.path.join("ok_result", file_name + 'result/')
result_number_not_ok_path = os.path.join("err_result", "single_exception" + file_name)  # 11为存在汉字
result_double_number_path = os.path.join("err_result", "double_exception" + file_name)   # 22位或者存在更多的汉字
print(file_name)
if not os.path.exists(result_path):
    os.mkdir(result_path)
if not os.path.exists(result_number_not_ok_path):
    os.mkdir(result_number_not_ok_path)
if not os.path.exists(result_double_number_path):
    os.mkdir(result_double_number_path)


def ocr_mark():
    images_path = os.listdir(path)
    num = 0
    random.shuffle(images_path)
    for image, i in zip(images_path, range(len(images_path))):
        start_time = time.time()
        img_name = image[:-4]
        img_path = os.path.join(path, image)
        img = open(img_path, "rb").read()
        b64 = base64.b64encode(img)
        data = {
            'access_token': '24.5895b543d4a9369a9b19a850f75f846d.2592000.1564468706.282335-16665908',
            'image': b64
        }
        url1 = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'     # 通用
        # url2 = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'    # 高精度
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            resp = requests.post(url=url1, headers=headers, data=data)
        except RequestException as e:
            print(e)
        # error_code 或者识别不出来的数据,
        if len(resp.json()) == 0 or len(resp.json()) <= 2 or 'words_result' not in resp.json() or len(resp.json()["words_result"]) <= 0:
            # open(os.path.join(result_err_path, image), 'wb').write(img)
            os.remove(os.path.join(path, image))
            continue
        phone = resp.json()["words_result"][0]["words"]
        print(phone, len(phone))
        phone2 = phone
        flag = 0
        for word in phone:
            if ord(word) < 48 or ord(word) > 57:
                phone = phone.replace(word, '')
        # 识别结果为11数字
        if len(phone) == 11:
            flag = 1
        # 正好10数字首位缺失
        elif len(phone) == 10:
            phone = list(phone)
            phone.insert(0, '1')
            phone = ''.join(phone)
            flag = 2
        # 识别结果大于11位数字
        elif len(phone) > 11:
            if len(phone) == 22:
                phone1 = phone[11:]
                if phone1 == phone[:11]:
                    phone = phone[:11]
                    flag = 3
            elif len(phone) > 11 and len(phone) < 22:
                if phone[0] == '1':
                    phone1 = phone[:11]
                    if phone[11:] == phone1[:len(phone) - 11] and len(phone[11:]) > 2:
                        flag = 3
                        phone = phone1
                else:
                    phone1 = phone[len(phone) - 11:]
                    if phone1[11 - len(phone[:len(phone) - 11]):] == phone[:len(phone) - 11] \
                            and len(phone[:len(phone) - 11]) > 2:
                        flag = 3
                        phone = phone1
        else:
            os.remove(os.path.join(path, image))
            continue
        g_phone = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                   '145', '147', '149', '150', '151', '152', '153', '155', '156', '157',
                   '158', '159', '166', '171', '172', '175', '176', '177', '178', '180',
                   '181', '182', '183', '184', '185', '186', '187', '188', '189', '198', '199']
        if flag != 0 and phone[:3] in g_phone:
            name = img_name + "_" + phone + ".jpg"
            num += 1
            print("第{}张图片，耗时{}秒，识别结果为:{}".format(i + 1, time.time() - start_time, phone2))
            if flag == 1:
                open(os.path.join(result_path, name), 'wb').write(img)
            elif flag == 2:
                open(os.path.join(result_number_not_ok_path, name), 'wb').write(img)
            else:
                open(os.path.join(result_double_number_path, name), 'wb').write(img)
        os.remove(os.path.join(path, image))
    print("{}张图片中识别成功的有{}张".format(len(images_path), num))


if __name__ == '__main__':
    ocr_mark()
