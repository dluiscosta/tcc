import numpy
import cv2
from math import exp

import sys

from paths_names import ORIGINALS, GRAYSCALE, REDSCALE, GREENSCALE, BLUESCALE, RESULTS, RESULTS_GRAY, RESULTS_RED, RESULTS_GREEN, RESULTS_BLUE

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

# B=151 a=111

def qsigmoid(old, B, a, q):
    D = abs((old - B)/a) + 0.0001

    if q != 1:
        if (1 + (1-q) * D) < 0:
            D = -1/D
        expq = 255/((1 + (1-q) * D)**(1/(1-q)))
    else:
        expq = 255 - (255/(1 + exp(-D)))

    expq = 0 if expq <= 0 else expq
    expq = 255 if numpy.isinf(expq) else expq

    return expq

# B = sys.argv[1]
# A = sys.argv[2]
image_num = sys.argv[1]

filename_gray = GRAYSCALE + 'gray_scale' + image_num + '.png'
filename_red = REDSCALE + 'red_scale' + image_num + '.png'
filename_green = GREENSCALE + 'green_scale' + image_num + '.png'
filename_blue = BLUESCALE + 'blue_scale' + image_num + '.png'


# B values for gray, red, green, blue
B = [217, 214,196, 210]

# A values for gray, red, green, blue
A = [110, 114,105, 156]

image_gray = read_image_grey_scale(filename_gray)
image_red = read_image_grey_scale(filename_red)
image_green = read_image_grey_scale(filename_green)
image_blue = read_image_grey_scale(filename_blue)

image_gray01 = image_gray.copy()
image_gray03 = image_gray.copy()
image_gray05 = image_gray.copy()
image_gray08 = image_gray.copy()
image_gray10 = image_gray.copy()
image_gray12 = image_gray.copy()
image_gray15 = image_gray.copy()
image_gray20 = image_gray.copy()
image_gray30 = image_gray.copy()

image_red01 = image_red.copy()
image_red03 = image_red.copy()
image_red05 = image_red.copy()
image_red08 = image_red.copy()
image_red10 = image_red.copy()
image_red12 = image_red.copy()
image_red15 = image_red.copy()
image_red20 = image_red.copy()
image_red30 = image_red.copy()

image_green01 = image_green.copy()
image_green03 = image_green.copy()
image_green05 = image_green.copy()
image_green08 = image_green.copy()
image_green10 = image_green.copy()
image_green12 = image_green.copy()
image_green15 = image_green.copy()
image_green20 = image_green.copy()
image_green30 = image_green.copy()

image_blue01 = image_blue.copy()
image_blue03 = image_blue.copy()
image_blue05 = image_blue.copy()
image_blue08 = image_blue.copy()
image_blue10 = image_blue.copy()
image_blue12 = image_blue.copy()
image_blue15 = image_blue.copy()
image_blue20 = image_blue.copy()
image_blue30 = image_blue.copy()

height, width = get_size_image(image_gray)

for i in range(0, height):
    for j in range(0, width):

        # gray images
        image_gray01.itemset((i,j), qsigmoid(image_gray[i,j], B[0], A[0], 0.1))
        image_gray03.itemset((i,j), qsigmoid(image_gray[i,j], B[0], A[0], 0.3))
        image_gray05.itemset((i,j), qsigmoid(image_gray[i,j], B[0], A[0], 0.5))
        image_gray08.itemset((i,j), qsigmoid(image_gray[i,j], B[0], A[0], 0.8))
        image_gray10.itemset((i,j), qsigmoid(image_gray[i,j], B[0], A[0], 1.0))
        image_gray12.itemset((i,j), qsigmoid(image_gray[i,j], B[0], A[0], 1.2))
        image_gray15.itemset((i,j), qsigmoid(image_gray[i,j], B[0], A[0], 1.5))
        image_gray20.itemset((i,j), qsigmoid(image_gray[i,j], B[0], A[0], 2.0))
        image_gray30.itemset((i,j), qsigmoid(image_gray[i,j], B[0], A[0], 3.0))

        # red images
        image_red01.itemset((i,j), qsigmoid(image_red[i,j], B[1], A[1], 0.1))
        image_red03.itemset((i,j), qsigmoid(image_red[i,j], B[1], A[1], 0.3))
        image_red05.itemset((i,j), qsigmoid(image_red[i,j], B[1], A[1], 0.5))
        image_red08.itemset((i,j), qsigmoid(image_red[i,j], B[1], A[1], 0.8))
        image_red10.itemset((i,j), qsigmoid(image_red[i,j], B[1], A[1], 1.0))
        image_red12.itemset((i,j), qsigmoid(image_red[i,j], B[1], A[1], 1.2))
        image_red15.itemset((i,j), qsigmoid(image_red[i,j], B[1], A[1], 1.5))
        image_red20.itemset((i,j), qsigmoid(image_red[i,j], B[1], A[1], 2.0))
        image_red30.itemset((i,j), qsigmoid(image_red[i,j], B[1], A[1], 3.0))

        # green images
        image_green01.itemset((i,j), qsigmoid(image_green[i,j], B[2], A[2], 0.1))
        image_green03.itemset((i,j), qsigmoid(image_green[i,j], B[2], A[2], 0.3))
        image_green05.itemset((i,j), qsigmoid(image_green[i,j], B[2], A[2], 0.5))
        image_green08.itemset((i,j), qsigmoid(image_green[i,j], B[2], A[2], 0.8))
        image_green10.itemset((i,j), qsigmoid(image_green[i,j], B[2], A[2], 1.0))
        image_green12.itemset((i,j), qsigmoid(image_green[i,j], B[2], A[2], 1.2))
        image_green15.itemset((i,j), qsigmoid(image_green[i,j], B[2], A[2], 1.5))
        image_green20.itemset((i,j), qsigmoid(image_green[i,j], B[2], A[2], 2.0))
        image_green30.itemset((i,j), qsigmoid(image_green[i,j], B[2], A[2], 3.0))

        # blue images
        image_blue01.itemset((i,j), qsigmoid(image_blue[i,j], B[3], A[3], 0.1))
        image_blue03.itemset((i,j), qsigmoid(image_blue[i,j], B[3], A[3], 0.3))
        image_blue05.itemset((i,j), qsigmoid(image_blue[i,j], B[3], A[3], 0.5))
        image_blue08.itemset((i,j), qsigmoid(image_blue[i,j], B[3], A[3], 0.8))
        image_blue10.itemset((i,j), qsigmoid(image_blue[i,j], B[3], A[3], 1.0))
        image_blue12.itemset((i,j), qsigmoid(image_blue[i,j], B[3], A[3], 1.2))
        image_blue15.itemset((i,j), qsigmoid(image_blue[i,j], B[3], A[3], 1.5))
        image_blue20.itemset((i,j), qsigmoid(image_blue[i,j], B[3], A[3], 2.0))
        image_blue30.itemset((i,j), qsigmoid(image_blue[i,j], B[3], A[3], 3.0))

# print (RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__01.png')

# write gray_images
cv2.imwrite((RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__01.png'), image_gray01)
cv2.imwrite((RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__03.png'), image_gray03)
cv2.imwrite((RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__05.png'), image_gray05)
cv2.imwrite((RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__08.png'), image_gray08)
cv2.imwrite((RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__10.png'), image_gray10)
cv2.imwrite((RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__12.png'), image_gray12)
cv2.imwrite((RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__15.png'), image_gray15)
cv2.imwrite((RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__20.png'), image_gray20)
cv2.imwrite((RESULTS + image_num + RESULTS_GRAY + image_num + '_gray__30.png'), image_gray30)

# write red_images
cv2.imwrite((RESULTS + image_num + RESULTS_RED + image_num + '_red__01.png'), image_red01)
cv2.imwrite((RESULTS + image_num + RESULTS_RED + image_num + '_red__03.png'), image_red03)
cv2.imwrite((RESULTS + image_num + RESULTS_RED + image_num + '_red__05.png'), image_red05)
cv2.imwrite((RESULTS + image_num + RESULTS_RED + image_num + '_red__08.png'), image_red08)
cv2.imwrite((RESULTS + image_num + RESULTS_RED + image_num + '_red__10.png'), image_red10)
cv2.imwrite((RESULTS + image_num + RESULTS_RED + image_num + '_red__12.png'), image_red12)
cv2.imwrite((RESULTS + image_num + RESULTS_RED + image_num + '_red__15.png'), image_red15)
cv2.imwrite((RESULTS + image_num + RESULTS_RED + image_num + '_red__20.png'), image_red20)
cv2.imwrite((RESULTS + image_num + RESULTS_RED + image_num + '_red__30.png'), image_red30)

# write green_images
cv2.imwrite((RESULTS + image_num + RESULTS_GREEN + image_num + '_green__01.png'), image_green01)
cv2.imwrite((RESULTS + image_num + RESULTS_GREEN + image_num + '_green__03.png'), image_green03)
cv2.imwrite((RESULTS + image_num + RESULTS_GREEN + image_num + '_green__05.png'), image_green05)
cv2.imwrite((RESULTS + image_num + RESULTS_GREEN + image_num + '_green__08.png'), image_green08)
cv2.imwrite((RESULTS + image_num + RESULTS_GREEN + image_num + '_green__10.png'), image_green10)
cv2.imwrite((RESULTS + image_num + RESULTS_GREEN + image_num + '_green__12.png'), image_green12)
cv2.imwrite((RESULTS + image_num + RESULTS_GREEN + image_num + '_green__15.png'), image_green15)
cv2.imwrite((RESULTS + image_num + RESULTS_GREEN + image_num + '_green__20.png'), image_green20)
cv2.imwrite((RESULTS + image_num + RESULTS_GREEN + image_num + '_green__30.png'), image_green30)

# write blue_images
cv2.imwrite((RESULTS + image_num + RESULTS_BLUE + image_num + '_blue__01.png'), image_blue01)
cv2.imwrite((RESULTS + image_num + RESULTS_BLUE + image_num + '_blue__03.png'), image_blue03)
cv2.imwrite((RESULTS + image_num + RESULTS_BLUE + image_num + '_blue__05.png'), image_blue05)
cv2.imwrite((RESULTS + image_num + RESULTS_BLUE + image_num + '_blue__08.png'), image_blue08)
cv2.imwrite((RESULTS + image_num + RESULTS_BLUE + image_num + '_blue__10.png'), image_blue10)
cv2.imwrite((RESULTS + image_num + RESULTS_BLUE + image_num + '_blue__12.png'), image_blue12)
cv2.imwrite((RESULTS + image_num + RESULTS_BLUE + image_num + '_blue__15.png'), image_blue15)
cv2.imwrite((RESULTS + image_num + RESULTS_BLUE + image_num + '_blue__20.png'), image_blue20)
cv2.imwrite((RESULTS + image_num + RESULTS_BLUE + image_num + '_blue__30.png'), image_blue30)
