import numpy as np
from PIL import Image

CONTENT_SIZE = 20, 20
FINAL_SIZE = 28, 28
TRESHOLD = 200

def load_image_as_grayscale(image_path):
    return Image.open(image_path).convert('L')


def process_image(image):
    img_as_array = np.asarray(image)
    x1, y1, w, h = find_border(img_as_array)
    img_as_array = img_as_array[y1:y1 + h, x1:x1 + w]

    single_digit_img = Image.fromarray(img_as_array, mode='L')

    single_digit_img.thumbnail(CONTENT_SIZE)

    center_x, center_y = find_center(single_digit_img)
    x2 = int(FINAL_SIZE[0] / 2 - center_x) - 1
    y2 = int(FINAL_SIZE[1] / 2 - center_y) - 1

    new_img_as_array = np.full(FINAL_SIZE, 255, np.uint8)

    new_img_as_array[y2:y2 + single_digit_img.height, x2:x2 + single_digit_img.width] = np.asarray(
        single_digit_img)

    return Image.fromarray(new_img_as_array, mode='L')


def find_border(img_as_array):
    y = -1
    for i in range(img_as_array.shape[0]):
        for j in range(img_as_array.shape[1]):
            if img_as_array[i][j] < TRESHOLD:
                y = i
                break
        if y >= 0:
            break
    h = -1
    for i in range(img_as_array.shape[0] - 1, -1, -1):
        for j in range(img_as_array.shape[1]):
            if img_as_array[i][j] < TRESHOLD:
                h = i - y
                break
        if h >= 0:
            break

    x = -1
    for j in range(img_as_array.shape[1]):
        for i in range(img_as_array.shape[0]):
            if img_as_array[i][j] < TRESHOLD:
                x = j
                break
        if x >= 0:
            break
    w = -1
    for j in range(img_as_array.shape[1] - 1, -1, -1):
        for i in range(img_as_array.shape[0]):
            if img_as_array[i][j] < TRESHOLD:
                w = j - x
                break
        if w >= 0:
            break

    return x, y, w, h

def find_center(img):
    image_as_array = 255 - np.asarray(img, np.uint8)
    x = 0.0
    y = 0.0
    mw = image_as_array.sum()

    for i in range(image_as_array.shape[0]):
        for j in range(image_as_array.shape[1]):
            x += j * image_as_array[i, j]
            y += i * image_as_array[i, j]

    return int(x / mw), int(y / mw)
