import sys
import cv2
import cv2.cv

def show_image(image, image_name):
    y, x = image.shape[0:2]
    show_image = cv2.resize(image, (int(0.2*x), int(0.2*y)))
    cv2.imshow(image_name, show_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


input_filename = sys.argv[1] 
if len(sys.argv) >= 3:
    output_filename = sys.argv[2] 
else:
    output_filename = "lamina_" + input_filename


image = cv2.imread(input_filename, cv2.IMREAD_GRAYSCALE)



circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 
                           1, 
                           minDist=image.shape[0]/8,
                           param2=100,
                           minRadius=image.shape[0]/3,
                           maxRadius=image.shape[0]/2
                           )

for i in range(0, len(circles[0])):
    center =  (int(circles[0][i][0]), int(circles[0][i][1])) 
    cv2.circle(image, center, int(circles[0][i][2]), (255, 0, 0), 3)
show_image(image, "Circulos")




cv2.imwrite(output_filename, image)