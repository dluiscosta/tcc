import matplotlib.pyplot as pyplot
from matplotlib.cbook import get_sample_data
import cv2
import numpy

from paths_names import ORIGINALS, REDSCALE, BLUESCALE, GREENSCALE, REDSCALE, GRAYSCALE

for i in range(1, 31):

    original = ORIGINALS + 'cropped_image' + str(i) +'.png'

    red_filename = REDSCALE + 'red_scale' + str(i) + '.png'

    green_filename = GREENSCALE + 'green_scale' + str(i) + '.png'

    blue_filename = BLUESCALE + 'blue_scale' + str(i) + '.png'

    gray_filename = GRAYSCALE + 'gray_scale' + str(i) + '.png'

    image = cv2.imread(original)

    gray = cv2.imread(original, cv2.IMREAD_GRAYSCALE)
    blue, green, red = image[:,:,0], image[:,:,1], image[:,:,2]

    cv2.imwrite(green_filename,green)
    cv2.imwrite(blue_filename,blue)
    cv2.imwrite(red_filename,red)
    cv2.imwrite(gray_filename, gray)
