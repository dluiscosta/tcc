import cv2
import cv2.cv
import math
import numpy as np
from screeninfo import get_monitors
    
def show_image(image, image_name):
    height, width = image.shape[0:2]
    cv2.namedWindow(image_name, cv2.WINDOW_NORMAL) 
    
    #Redimensiona a imagem para que caiba na tela, sem distorcoes
    monitor = get_monitors()[0]
    fator = min(monitor.width/float(width), monitor.height/float(height), 1)
    cv2.resizeWindow(image_name, int(width*fator), int(height*fator))
    
    #Exibe a imagem
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_multiple_images(images, window_name):
    if len(images) > 6:
        print "Muitas imagens para exibir."
        return
    formato = [(1,1), (2,1), (3,1), (2,2), (3,2), (3,2)]
    cols, rows = formato[len(images)-1]
    height, width = images[0].shape[0:2] #assume que as imagens tem o mesmo tamanho
    container = np.zeros((int(height*rows), int(width*cols), 3), np.uint8)
    for i in range(0, len(images)):
        x = int(i%cols)
        y = int(math.floor(i/cols))
        container[y*height:(y+1)*height,x*width:(x+1)*width] = images[i]
    show_image(container, window_name)

