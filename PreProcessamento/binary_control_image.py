import numpy
import cv2
from math import exp

import sys

def read_image_grey_scale(file_name):
    return cv2.imread(file_name, 0)

def get_size_image(image):
    return image.shape

def show_image(image, image_name):
    y, x = get_size_image(image)
    show_image = cv2.resize(image, (int(0.2*x), int(0.2*y)))
    cv2.imshow(image_name, show_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

control_image_name = '/home/nayara/ARTIGO-PS/CONTROL_IMAGES/control_image1.png'

control_image = read_image_grey_scale(control_image_name)
height, width = get_size_image(control_image)
binary_image = control_image.copy()

for i in range(0, height):
    for j in range(0, width):
        binary_image.itemset((i, j), 255 if binary_image[i, j] < 245 else 0)

cv2.imwrite('BINARY2.png', binary_image)
