import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def show_image(img):
    plt.imshow(img, cmap='Greys')
    plt.show()
    pass


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


class DataSet:

    def __init__(self):
        self.result_array = None
        self.input_array = None
        self.sizeX = 191
        self.sizeY = 158
        self.marginX = 10
        self.marginY = 15
        self.treshold = 200

    def create_data_set(self, image_path):
        img = Image.open(image_path)  # 1918x3166
        # self.show_image(img)
        self.split_image(img.convert('L'))

    def split_image(self, img):
        for y in range(20):
            for x in range(10):
                x1 = x * self.sizeX + self.marginX
                x2 = (x + 1) * self.sizeX - self.marginX
                y1 = y * self.sizeY + self.marginY
                y2 = (y + 1) * self.sizeY - self.marginY

                img_as_array = np.asarray(img, np.uint8)[y1:y2, x1:x2]
                image = self.process_image(img_as_array)

                path = "pictures\\Digit" + str(int(y / 2)) + "_" + str(10 * (y % 2) + x + 1) + ".png"
                print(path)
                image.save(path, "PNG")

    def process_image(self, img_as_array, mode='weight'):

        x1, y1, w, h = self.find_border(img_as_array)

        img_as_array = img_as_array[y1:y1 + h, x1:x1 + w]
        single_digit_img = Image.fromarray(img_as_array, mode='1')
        single_digit_img = single_digit_img.convert(mode='L')
        # self.show_image(single_digit_img)

        content_size = 20, 20
        single_digit_img.thumbnail(content_size)  # resizes image in-place
        # self.show_image(single_digit_img)

        final_size = 28, 28
        new_img_as_array = np.full(final_size, 255, np.uint8)
        if mode == 'weight':
            center_x, center_y = find_center(single_digit_img)
            x2 = int(final_size[0] / 2 - center_x) - 1
            y2 = int(final_size[1] / 2 - center_y) - 1
        else:
            x2 = int((final_size[0] - single_digit_img.width) / 2)
            y2 = int((final_size[1] - single_digit_img.height) / 2)

        new_img_as_array[y2:y2 + single_digit_img.height, x2:x2 + single_digit_img.width] = np.asarray(
            single_digit_img)

        single_digit_img = Image.fromarray(new_img_as_array, mode='L')
        # self.show_image(single_digit_img)

        return single_digit_img

    def find_border(self, img_as_array):
        y = -1
        for i in range(img_as_array.shape[0]):
            for j in range(img_as_array.shape[1]):
                if img_as_array[i][j] < self.treshold:
                    y = i
                    break
            if y >= 0:
                break
        h = -1
        for i in range(img_as_array.shape[0] - 1, -1, -1):
            for j in range(img_as_array.shape[1]):
                if img_as_array[i][j] < self.treshold:
                    h = i - y
                    break
            if h >= 0:
                break

        x = -1
        for j in range(img_as_array.shape[1]):
            for i in range(img_as_array.shape[0]):
                if img_as_array[i][j] < self.treshold:
                    x = j
                    break
            if x >= 0:
                break
        w = -1
        for j in range(img_as_array.shape[1] - 1, -1, -1):
            for i in range(img_as_array.shape[0]):
                if img_as_array[i][j] < self.treshold:
                    w = j - x
                    break
            if w >= 0:
                break

        return x, y, w, h

    def load_data(self):
        files = os.listdir('pictures')

        n = 0
        self.input_array = np.zeros((len(files), 28 * 28), np.int16)
        self.result_array = np.zeros((len(files), 10), np.int16)

        for f in files:
            if f.startswith('Digit'):
                self.result_array[n][int(f[f.find('t') + 1:f.find('t') + 2])] = 1
                image_array = np.asarray(Image.open('pictures\\' + f))
                k = 0
                for i in range(len(image_array)):
                    for j in range(len(image_array[0])):
                        self.input_array[n][k] = image_array[i][j]
                        k += 1
                n = n + 1
                print('trainingdata\\' + f)

    def get_data_set(self):
        return self.input_array, self.result_array

    def save_datset(self):
        np.savetxt('trainingdata.csv', self.input_array, fmt='%d')
        np.savetxt('resultdata.csv', self.result_array, fmt='%d')
