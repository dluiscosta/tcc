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


#Exibe os passos do procedimento
if args.analise:
    show_multiple_images(steps, "Passo a passo")
    

#Se especificado, salva a imagem de saída
if args.salvar != None:
    cv2.imwrite(args.salvar, mask[1])