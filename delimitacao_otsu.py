import cv2
import cv2.cv
import argparse
from exibir_imagens import mostra_imagens
import numpy as np

def delimitacao_otsu(imagem, analise=False, removeEspurias=True, encaixaCirculo=True):
    if analise:
        print "- Delimitacao por limiarizacao de Otsu -"
        mostra_imagens([imagem], "", ["Imagem de entrada, apenas um canal"])
        
    #Binarizacao por Otsu
    limiar, binaria = cv2.threshold(imagem, 0, 255, 
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

#Parser de parametros do script
parser = argparse.ArgumentParser(description="Delimita a regiao circular da lamina.")
parser.add_argument("-i", "--input", help="Nome do arquivo da imagem de entrada.", action="store")
parser.add_argument("-s", "--salvar", help="Nome do arquivo da imagem de saida.", action="store")
parser.add_argument("-a", "--analise", help="Modo de analise.", action="store_true")
args = parser.parse_args()

#Abre a imagem de entrada e considera apenas o canal azul
input_filename = args.input
if input_filename is not None:
    imagem = cv2.imread(input_filename, cv2.IMREAD_COLOR)[:,:,0]

    binaria = delimitacao_otsu(imagem, args.analise)
    
    #Se especificado, salva a imagem de saida
    if args.salvar != None:
        cv2.imwrite(args.salvar, binaria)