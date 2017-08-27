import cv2
import numpy

from paths_names import RESULTS_BLUE, RESULTS, RESULTS_GREEN, RESULTS_RED, RESULTS_GRAY

def read_image_grey_scale(file_name):
    return cv2.imread(file_name, 0)

def get_size_image(image):
    return image.shape

path_bluescale = RESULTS + '{}' + RESULTS_BLUE
path_greenscale = RESULTS + '{}' + RESULTS_GREEN
path_redscale = RESULTS + '{}' + RESULTS_RED
path_grayscale = RESULTS + '{}' + RESULTS_GRAY

image_blue_name01 = path_grayscale + '{}' + '_gray__01.png'
image_blue_name03 = path_grayscale + '{}' + '_gray__03.png'
image_blue_name05 = path_grayscale + '{}' + '_gray__05.png'
image_blue_name08 = path_grayscale + '{}' + '_gray__08.png'
image_blue_name10 = path_grayscale + '{}' + '_gray__10.png'
image_blue_name12 = path_grayscale + '{}' + '_gray__12.png'
image_blue_name15 = path_grayscale + '{}' + '_gray__15.png'
image_blue_name20 = path_grayscale + '{}' + '_gray__20.png'
image_blue_name30 = path_grayscale + '{}' + '_gray__30.png'

# otsu
image_blue_name01_otsu = path_grayscale + '{}' + '_gray__01_otsu.png'
image_blue_name03_otsu = path_grayscale + '{}' + '_gray__03_otsu.png'
image_blue_name05_otsu = path_grayscale + '{}' + '_gray__05_otsu.png'
image_blue_name08_otsu = path_grayscale + '{}' + '_gray__08_otsu.png'
image_blue_name10_otsu = path_grayscale + '{}' + '_gray__10_otsu.png'
image_blue_name12_otsu = path_grayscale + '{}' + '_gray__12_otsu.png'
image_blue_name15_otsu = path_grayscale + '{}' + '_gray__15_otsu.png'
image_blue_name20_otsu = path_grayscale + '{}' + '_gray__20_otsu.png'
image_blue_name30_otsu = path_grayscale + '{}' + '_gray__30_otsu.png'

# otsu + gauss
image_blue_name01_gauss = path_grayscale + '{}' + '_gray__01_gauss.png'
image_blue_name03_gauss = path_grayscale + '{}' + '_gray__03_gauss.png'
image_blue_name05_gauss = path_grayscale + '{}' + '_gray__05_gauss.png'
image_blue_name08_gauss = path_grayscale + '{}' + '_gray__08_gauss.png'
image_blue_name10_gauss = path_grayscale + '{}' + '_gray__10_gauss.png'
image_blue_name12_gauss = path_grayscale + '{}' + '_gray__12_gauss.png'
image_blue_name15_gauss = path_grayscale + '{}' + '_gray__15_gauss.png'
image_blue_name20_gauss = path_grayscale + '{}' + '_gray__20_gauss.png'
image_blue_name30_gauss = path_grayscale + '{}' + '_gray__30_gauss.png'

# print(image_blue_name01.format(1,1))
# print(image_blue_name30_otsu.format(1,1))
# print(image_blue_name01_gauss.format(1,1))


for i in range (1, 22):
    image_01 = read_image_grey_scale(image_blue_name01.format(i,i))
    image_03 = read_image_grey_scale(image_blue_name03.format(i,i))
    image_05 = read_image_grey_scale(image_blue_name05.format(i,i))
    image_08 = read_image_grey_scale(image_blue_name08.format(i,i))
    image_10 = read_image_grey_scale(image_blue_name10.format(i,i))
    image_12 = read_image_grey_scale(image_blue_name12.format(i,i))
    image_15 = read_image_grey_scale(image_blue_name15.format(i,i))
    image_20 = read_image_grey_scale(image_blue_name20.format(i,i))
    image_30 = read_image_grey_scale(image_blue_name30.format(i,i))
    # binary_image = control_image.copy()

    blur_01 = cv2.GaussianBlur(image_01,(5,5),0)
    ret1, otsu_image_01 = cv2.threshold(image_01, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1, gauss_image_01 = cv2.threshold(blur_01, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    blur_03 = cv2.GaussianBlur(image_03,(5,5),0)
    ret1, otsu_image_03 = cv2.threshold(image_03, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1, gauss_image_03 = cv2.threshold(blur_03, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    blur_05 = cv2.GaussianBlur(image_05,(5,5),0)
    ret1, otsu_image_05 = cv2.threshold(image_05, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1, gauss_image_05 = cv2.threshold(blur_05, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    blur_08 = cv2.GaussianBlur(image_08,(5,5),0)
    ret1, otsu_image_08 = cv2.threshold(image_08, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1, gauss_image_08 = cv2.threshold(blur_08, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    blur_10 = cv2.GaussianBlur(image_10,(5,5),0)
    ret1, otsu_image_10 = cv2.threshold(image_10, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1, gauss_image_10 = cv2.threshold(blur_10, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    blur_12 = cv2.GaussianBlur(image_12,(5,5),0)
    ret1, otsu_image_12 = cv2.threshold(image_12, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1, gauss_image_12 = cv2.threshold(blur_12, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    blur_15 = cv2.GaussianBlur(image_15,(5,5),0)
    ret1, otsu_image_15 = cv2.threshold(image_15, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1, gauss_image_15 = cv2.threshold(blur_15, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    blur_20 = cv2.GaussianBlur(image_20,(5,5),0)
    ret1, otsu_image_20 = cv2.threshold(image_20, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1, gauss_image_20 = cv2.threshold(blur_20, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    blur_30 = cv2.GaussianBlur(image_30,(5,5),0)
    ret1, otsu_image_30 = cv2.threshold(image_30, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1, gauss_image_30 = cv2.threshold(blur_30, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)


    cv2.imwrite(image_blue_name01_otsu.format(i,i), otsu_image_01)
    cv2.imwrite(image_blue_name01_gauss.format(i,i), gauss_image_01)

    cv2.imwrite(image_blue_name03_otsu.format(i,i), otsu_image_03)
    cv2.imwrite(image_blue_name03_gauss.format(i,i), gauss_image_03)

    cv2.imwrite(image_blue_name05_otsu.format(i,i), otsu_image_05)
    cv2.imwrite(image_blue_name05_gauss.format(i,i), gauss_image_05)

    cv2.imwrite(image_blue_name08_otsu.format(i,i), otsu_image_08)
    cv2.imwrite(image_blue_name08_gauss.format(i,i), gauss_image_08)

    cv2.imwrite(image_blue_name10_otsu.format(i,i), otsu_image_10)
    cv2.imwrite(image_blue_name10_gauss.format(i,i), gauss_image_10)

    cv2.imwrite(image_blue_name12_otsu.format(i,i), otsu_image_12)
    cv2.imwrite(image_blue_name12_gauss.format(i,i), gauss_image_12)

    cv2.imwrite(image_blue_name15_otsu.format(i,i), otsu_image_15)
    cv2.imwrite(image_blue_name15_gauss.format(i,i), gauss_image_15)

    cv2.imwrite(image_blue_name20_otsu.format(i,i), otsu_image_20)
    cv2.imwrite(image_blue_name20_gauss.format(i,i), gauss_image_20)

    cv2.imwrite(image_blue_name30_otsu.format(i,i), otsu_image_30)
    cv2.imwrite(image_blue_name30_gauss.format(i,i), gauss_image_30)
