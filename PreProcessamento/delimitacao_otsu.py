# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 21:48:38 2017

@author: Daniel
"""

import cv2
import cv2.cv
import argparse
import math
import numpy as np

def show_image(image, image_name):
    y, x = image.shape[0:2]
    show_image = cv2.resize(image, (int(0.2*x), int(0.2*y)))
    cv2.namedWindow(image_name, cv2.WINDOW_NORMAL) 
    cv2.imshow(image_name, show_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_multiple_images(images, window_name):
    height, width = images[0].shape[0:2] #assume que as imagens tem o mesmo tamanho
    a = int(math.ceil(math.sqrt(len(images))))
    container = np.zeros((int(height*a), int(width*a), 3), np.uint8)
    for i in range(0, len(images)):
        x = int(i%a)
        y = int(math.floor(i/a))
        container[y*height:(y+1)*height,x*width:(x+1)*width] = images[i]
    show_image(container, window_name)
    
#Parser de parâmetros do script
parser = argparse.ArgumentParser(description="Delimita a região circular da lâmina.")
parser.add_argument("input", help="Nome do arquivo da imagem de entrada.", action="store")
parser.add_argument("-s", "--salvar", help="Nome do arquivo da imagem de saída.", action="store")
parser.add_argument("-a", "--analise", help="Modo de análise", action="store_true")
args = parser.parse_args()

steps = []

#Abre a imagem de entrada e considera apenas o canal azul
input_filename = args.input
image = cv2.imread(input_filename, cv2.IMREAD_COLOR)[:,:,0]

if args.analise:
    steps.append(cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB))


#Binarização por Otsu
mask = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

if args.analise:
    steps.append(cv2.cvtColor(mask[1], cv2.cv.CV_GRAY2RGB))

#Exibe os passos do procedimento
if args.analise:
    show_multiple_images(steps, "Passo a passo")
    
#Se especificado, salva a imagem de saída
if args.salvar != None:
    cv2.imwrite(args.salvar, image)