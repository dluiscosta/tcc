import cv2
import cv2.cv
import argparse
from exibir_imagens import mostra_imagens
    
def extrair_regioes(imagem, analise=False):
    if analise:
        print "- Extracao de regioes conexas -"
        mostra_imagens([imagem], "", ["Imagem de entrada, apenas um canal"])
        
    #Encontra os contornos das regioes
    contours, hierarchy = cv2.findContours(imagem, 
            cv2.RETR_CCOMP, #associa contornos de componentes com contornos de buracos
            cv2.CHAIN_APPROX_NONE) #armazena todos os pontos no contorno

    if analise:
        import numpy
        import random
        #Desenha os contornos
        c = numpy.zeros((1, 1, 3), dtype=numpy.uint8) #imagem para conversao
        imagem_rgb = cv2.cvtColor(imagem, cv2.cv.CV_GRAY2RGB)
        for i in range(0, len(contours)):
            #Gera cor aleatória com saturacao e valor máximo, apenas alterando o hue.
            c[0][0] = [random.randint(0, 180), 100, 100] 
            c2 = cv2.cvtColor(c, cv2.COLOR_HSV2BGR)         
            color = numpy.array((int(c2[0][0][0]), int(c2[0][0][1]), int(c2[0][0][2])))   

            #So desenha o contorno se ele nao for filho de outro contorno.
            #Nesse caso, o contorno sera desenhado na vez do seu pai, 
            #com a mesma cor que ele
            if hierarchy[0,i,3] == -1: #nao tem pai
                cv2.drawContours(imagem_rgb, contours, i, color, 3)   
            #Se houverem filhos, os desenha.
            if hierarchy[0,i,2] != -1: #ha filho(s)
                indice = hierarchy[0,i,2] #primeiro filho
                cv2.drawContours(imagem_rgb, contours, indice, color, 3)  
                while hierarchy[0,indice,0] != -1: #itera pelos outros filhos
                    indice = hierarchy[0,indice,0]
                    cv2.drawContours(imagem_rgb, contours, indice, color, 3)  
                    
        mostra_imagens([imagem_rgb], "",
                       ["Contornos das regioes encontradas"])
        print "Contornos de mesma cor sao bordas externa e internas de um mesmo componente."
        
    return contours, hierarchy
                        
#Parser de parâmetros do script
parser = argparse.ArgumentParser(description="Extracao de regioes conexas. As regioes sao as brancas e o background preto.")
parser.add_argument("-i", "--input", help="Nome do arquivo da imagem de entrada, uma imagem binaria.", action="store")
parser.add_argument("-s", "--salvar", help="Contornos e hierarquia em um arquivo pickle.", action="store")
parser.add_argument("-a", "--analise", help="Modo de analise.", action="store_true")
args = parser.parse_args()

#Abre a imagem binaria de entrada
input_filename = args.input
if input_filename is not None:
    imagem = cv2.imread(input_filename, cv2.IMREAD_GRAYSCALE)
    
    contours, hierarchy = extrair_regioes(imagem, args.analise)
    
    #Se especificado, salva os contornos e a hierarquia
    if args.salvar != None:
        import pickle
        pickle.dump((contours, hierarchy), args.salvar)

