import cv2
import cv2.cv
from exibir_imagens import mostra_imagens
import numpy as np

def delimitacao_otsu(imagem, cor=0, removeEspurias=True, encaixaCirculo=True, analise=False):
    #Pega apenas o canal (ou a imagem em grayscale) especificado 
    im_c = imagem[:,:,cor] if cor <= 2 else cv2.cvtColor(imagem, cv2.cv.CV_BGR2GRAY)
        
    if analise:
        print "- Delimitacao por limiarizacao de Otsu -"
        mostra_imagens([im_c], "", ["Imagem de entrada, apenas um canal"])
        
    #Binarizacao por Otsu
    limiar, binaria = cv2.threshold(im_c, 0, 255, 
                                    cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    if analise:
        mostra_imagens([binaria], "",
                       ["Imagem binaria limiarizada em " + str(limiar)])
    
    if removeEspurias:
        #Remocao de regioes menores dentro ou fora da lamina
        contours, hierarchy = cv2.findContours(binaria, 
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        lamina = max(contours, key=cv2.contourArea) #assume que a lamina eh a regiao
        #com contorno de maior area
        
        binaria = np.zeros(binaria.shape, dtype=np.uint8)
        cv2.drawContours(binaria, [lamina], 0, 255, -1)

        if analise:
            mostra_imagens([binaria], "",
                       ["Apos remocao das regioes espurias"])
            
        if encaixaCirculo:
            M = cv2.moments(lamina) 
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            centro = (x, y)            
            import math
            raio = int(math.sqrt(cv2.contourArea(lamina)/math.pi))
            
            im = None
            if analise:
                #Indice, sobre a regiao original, onde estao o centro e perimetro
                #do circulo encaixados.
                im = cv2.cvtColor(binaria, cv2.cv.CV_GRAY2BGR)
                cv2.circle(im, centro, raio, (0, 0, 255), 3)
                cv2.circle(im, centro, 10, (0, 0, 255), -1)
                        
            binaria = np.zeros(binaria.shape, dtype=np.uint8)
            cv2.circle(binaria, centro, raio, 255, -1)
            
            if analise:
                mostra_imagens([im, binaria], "Circulo encaixado")
        
    return binaria