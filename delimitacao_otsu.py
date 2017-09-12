import cv2
import cv2.cv
import argparse
from exibir_imagens import show_multiple_images 
    
#Parser de parâmetros do script
parser = argparse.ArgumentParser(description="Delimita a região circular da lâmina.")
parser.add_argument("input", help="Nome do arquivo da imagem de entrada.", action="store")
parser.add_argument("-s", "--salvar", help="Nome do arquivo da imagem de saída.", action="store")
parser.add_argument("-a", "--analise", help="Modo de análise.", action="store_true")
args = parser.parse_args()


#Imagens a serem exibidas
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

'''
#Componentes conexos
from Queue import Queue
import numpy as np

label = 0
height, width = mask[1].shape
componentes_conexos = np.zeros(mask[1].shape)
f = Queue()
            
def expand(a, b):
    if b[0] >= 0 and b[1] >= 0 and b[0] < height and b[1] < width:
        if componentes_conexos[b] == 0 and mask[1][b] == mask[1][a]:
            componentes_conexos[b] = label    
            f.put(b)

for x in range(0, width):
    for y in range(0, height):
        if componentes_conexos[y][x] == 0:
            label += 1
            f.put((y, x))
            componentes_conexos[y][x] = label 
            while f.empty() == False:
                yi, xi = f.get()
                expand((yi, xi), (yi+1, xi+1))
                expand((yi, xi), (yi+1, xi-1))
                expand((yi, xi), (yi-1, xi+1))
                expand((yi, xi), (yi-1, xi-1))                    
#Ficou super lentíssimo
#Python eu te abomino!
'''

#Exibe os passos do procedimento
if args.analise:
    show_multiple_images(steps, "Passo a passo")
    

#Se especificado, salva a imagem de saída
if args.salvar != None:
    cv2.imwrite(args.salvar, mask[1])