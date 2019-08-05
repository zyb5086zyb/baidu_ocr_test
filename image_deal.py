import os
from PIL import Image, ImageEnhance
import cv2
import imutils
import numpy as np
import time


def enhance_image(image):
    image = cv2.imread(image, cv2.IMREAD_COLOR)
    image = Image.fromarray(image)

    img_bright = ImageEnhance.Brightness(image)
    brightness = 1.9
    image = img_bright.enhance(brightness)

    img_color = ImageEnhance.Color(image)
    colorness = 2.5
    image = img_color.enhance(colorness)

    img_contor = ImageEnhance.Contrast(image)
    contrast = 1.9
    image = img_contor.enhance(contrast)

    img_sharp = ImageEnhance.Sharpness(image)
    sharpness = 1.9
    image = img_sharp.enhance(sharpness)

    image = np.array(image)
    return image


def get_binary_image(image):
    # image = cv2.imread(image, cv2.IMREAD_COLOR)
    # image = cv2.resize(image, (400, 32))
    image = enhance_image(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 10)
    return image


def clear_line(image):
    stand_pixel = 20
    h, w = image.shape[:2]
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            count = 0
            if image[x, y - 1] > stand_pixel:
                count += 1
            if image[x, y + 1] > stand_pixel:
                count += 1
            if image[x - 1, y] > stand_pixel:
                count += 1
            if image[x + 1, y] > stand_pixel:
                count += 1
            if count > 2:
                image[x, y] = 255
    return image


def clear_point(image):
    stand_pixel = 54
    h, w = image.shape[:2]
    for y in range(0, w - 1):
        for x in range(0, h - 1):
            cur_pixel = image[x, y]
            if y == 0:
                if x == 0:
                    sum_pixel = int(cur_pixel) \
                                + int(image[x + 1, y]) \
                                + int(image[x, y + 1]) \
                                + int(image[x + 1, y + 1])
                    if sum_pixel <= 2 * stand_pixel:
                        image[x, y] = 0
                elif x == h - 1:
                    sum_pixel = int(cur_pixel) \
                                + int(image[x - 1, y])\
                                + int(image[x - 1, y]) \
                                + int(image[x, y + 1])
                    if sum_pixel <= 2 * stand_pixel:
                        image[x, y] = 0
                else:
                    sum_pixel = int(cur_pixel) \
                                + int(image[x - 1, y]) \
                                + int(image[x - 1, y + 1]) \
                                + int(image[x, y + 1]) \
                                + int(image[x + 1, y + 1]) \
                                + int(image[x + 1, y])
                    if sum_pixel <= 3 * stand_pixel:
                        image[x, y] = 0
            elif y == w - 1:
                if x == 0:
                    sum_pixel = int(cur_pixel)\
                                + int(image[x, y - 1]) \
                                + int(image[x + 1, y - 1]) \
                                + int(image[x + 1, y])
                    if sum_pixel <= 2 * stand_pixel:
                        image[x, y] = 0
                elif x == h - 1:
                    sum_pixel = int(cur_pixel) \
                                + int(image[x - 1, y]) \
                                + int(image[x - 1, y - 1]) \
                                + int(image[x, y - 1])
                    if sum_pixel <= 2 * stand_pixel:
                        image[x, y] = 0
                else:
                    sum_pixel = int(cur_pixel) + \
                                int(image[x - 1, y]) \
                                + int(image[x - 1, y - 1]) \
                                + int(image[x, y - 1]) \
                                + int(image[x + 1, y - 1])\
                                + int(image[x + 1, y])
                    if sum_pixel <= 3 * stand_pixel:
                        image[x, y] = 0
            else:
                sum_pixel = int(cur_pixel)\
                            + int(image[x - 1, y])\
                            + int(image[x - 1, y - 1]) \
                            + int(image[x, y - 1]) \
                            + int(image[x + 1, y - 1]) \
                            + int(image[x + 1, y]) \
                            + int(image[x + 1, y + 1]) \
                            + int(image[x, y + 1]) \
                            + int(image[x - 1, y + 1])
                if sum_pixel <= 4 * stand_pixel:
                    image[x, y] = 0
    return image


def clear_big_point(image, name):
    cnts = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for cnt in cnts:
        rect = cv2.minAreaRect(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        flag = 0
        print("w * h:{}".format(w * h))
        if w * h < 60:
            image[y:y+w, x:x+h] = 255
            flag = 1
        box = cv2.cv.boxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)
        if flag == 0:
            cv2.drawContours(image, [box], -1, (0, 0, 255), 1)
    print("---image----{}".format(name))
    return image


if __name__ == '__main__':
    images_path = "../images"
    output_path = "./result"
    image_path = os.listdir(images_path)
    for img_path in image_path:
        img = os.path.join(images_path, img_path)
        start_time = time.time()
        image = get_binary_image(img)
        image = clear_line(image)
        for i in range(4):
            image = clear_point(image)
        image = clear_big_point(image, img.split('/')[-1])
        print("耗时{}".format(time.time() - start_time))
        cv2.imwrite(os.path.join(output_path, img.split('/')[-1]), image)
