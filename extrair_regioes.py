import cv2
import cv2.cv
import argparse
from exibir_imagens import show_multiple_images 
    
#Parser de parâmetros do script
parser = argparse.ArgumentParser(description="Extração de regiões conexas. As regiões são as brancas e o background preto.")
parser.add_argument("input", help="Nome do arquivo da imagem de entrada, uma imagem binária.", action="store")
parser.add_argument("-s", "--salvar", help="OQ VAI SAIR?", action="store")
parser.add_argument("-a", "--analise", help="Modo de análise.", action="store_true")
args = parser.parse_args()


#Imagens a serem exibidas
steps = []


#Abre a imagem de entrada e considera apenas o canal azul
input_filename = args.input
image = cv2.imread(input_filename, cv2.IMREAD_GRAYSCALE)

if args.analise:
    steps.append(cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB))

#Encontra os contornos das regiões
contours, hierarchy = cv2.findContours(image, 
        cv2.RETR_CCOMP, #associa contornos de componentes com contornos de buracos
        cv2.CHAIN_APPROX_NONE) #armazena todos os pontos no contorno

if args.analise:
    import numpy
    import random
    #desenha os contornos
    c = numpy.zeros((1, 1, 3), dtype=numpy.uint8)
    image_rgb = cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB)
    for i in range(0, len(contours)):
        #gera cor aleatória com saturação e valor máximo, apenas alterando o hue
        c[0][0] = [random.randint(0, 180), 100, 100] 
        c2 = cv2.cvtColor(c, cv2.COLOR_HSV2BGR)         
        color = numpy.array((int(c2[0][0][0]), int(c2[0][0][1]), int(c2[0][0][2])))   
        #só desenha o contorno se ele não for filho de outro contorno
        #esse contorno será desenhado na vez do seu pai, com a mesma cor que ele
        if hierarchy[0,i,3] == -1: 
            cv2.drawContours(image_rgb, contours, i, color, 3)   
        #se houverem filhos, os desenha
        if hierarchy[0,i,2] != -1:
            indice = hierarchy[0,i,2] #primeiro filho
            cv2.drawContours(image_rgb, contours, indice, color, 3)  
            while hierarchy[0,indice,0] != -1: #proximos filhos
                indice = hierarchy[0,indice,0]
                cv2.drawContours(image_rgb, contours, indice, color, 3)  
            
    steps.append(image_rgb)
                                 
#Exibe os passos do procedimento
if args.analise:
    show_multiple_images(steps, "Passo a passo")

#Se especificado, salva a imagem de saída
if args.salvar != None:
    cv2.imwrite(args.salvar, image_rgb)

