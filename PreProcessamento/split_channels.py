import matplotlib.pyplot as pyplot
from matplotlib.cbook import get_sample_data
import cv2
import numpy

for i in range(1, 5):

    original = 'cropped_image' + str(i) +'.jpg'

    red_filename = 'red_scale' + str(i) + '.jpg'

    green_filename = 'green_scale' + str(i) + '.jpg'

    blue_filename = 'blue_scale' + str(i) + '.jpg'

    gray_filename = 'gray_scale' + str(i) + '.jpg'


    print(original)
    
    image = cv2.imread(original)

    gray = cv2.imread(original, cv2.IMREAD_GRAYSCALE)
    blue, green, red = image[:,:,0], image[:,:,1], image[:,:,2]

    cv2.imwrite(green_filename,green)
    cv2.imwrite(blue_filename,blue)
    cv2.imwrite(red_filename,red)
    cv2.imwrite(gray_filename, gray)
