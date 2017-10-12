import cv2
import cv2.cv
import math
import numpy as np

#Mostra n imagens lado a lado.
def mostra_imagens(imagens, titulo, subtitulos=[]):
    from matplotlib import pyplot as plt
    figura = plt.figure()
    for i in range(0, len(imagens)):
        #se o formato de entrada for GRAYSCALE, converte para RGB
        if len(imagens[i].shape) == 2:
            imagens[i] = cv2.cvtColor(imagens[i], cv2.cv.CV_GRAY2RGB)
        else:
            imagens[i] = cv2.cvtColor(imagens[i], cv2.cv.CV_BGR2RGB)
            
        subplot = figura.add_subplot(1, len(imagens), i+1)
        subplot.axis('off')
        if i < len(subtitulos):
            subplot.set_title(subtitulos[i])
        subplot.imshow(imagens[i])
    plt.suptitle(titulo)
    plt.show()

'''
def mostra_imagem(imagem, titulo):
    from matplotlib import pyplot as plt
    if not isinstance(imagem[0,0], (list, tuple)):
        imagem = cv2.cvtColor(imagem, cv2.cv.CV_GRAY2RGB)
        
    plt.figure()
    plt.axis('off')
    plt.title(titulo)
    plt.imshow(imagem)
    plt.show()


def show_image(image, image_name):
    from screeninfo import get_monitors
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

'''