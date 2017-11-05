import cv2
import cv2.cv

def limiarizacao(imagem, lamina, cor=1, limiar=146, analise=False):
    #Pega apenas o canal (ou a imagem em grayscale) especificado
    im_c = imagem[:,:,cor] if cor <= 2 else cv2.cvtColor(imagem, cv2.cv.CV_BGR2GRAY)
    
    #Limiariza no valor especificado; 
    #pixels de intensidade inferior ou igual a do limiar passam a compor o foreground.
    l, im_b = cv2.threshold(im_c, limiar, 255, cv2.THRESH_BINARY_INV)
    
    #Aplica a mascara da lamina, removendo as regioes do foreground 
    #que sejam exteriores a lamina
    im_b[lamina == 0] = 0 
    
    return im_b