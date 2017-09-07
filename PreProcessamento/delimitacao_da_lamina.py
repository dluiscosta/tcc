import cv2
import cv2.cv
import argparse
import math
import numpy as np

def show_image(image, image_name):
    y, x = image.shape[0:2]
    show_image = cv2.resize(image, (int(0.2*x), int(0.2*y)))
    cv2.imshow(image_name, show_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_multiple_images(images, window_name):
    height, width = images[0].shape[0:2] #assume que as imagens tem o mesmo tamanho
    print height
    print width
    a = int(math.ceil(math.sqrt(len(images))))
    container = np.zeros((int(height*a), int(width*a), 3), np.uint8)
    for i in range(0, len(images)):
        x = i%a
        y = int(math.floor(i/a))
        print y*a
        print y*a+height
        container[y*a:y*a+height][x*a:x*a+width] = images[i]
    show_image(container, window_name)
    
#Parser de parâmetros do script
parser = argparse.ArgumentParser(description="Delimita a região circular da lâmina.")
parser.add_argument("input", help="Nome do arquivo da imagem de entrada.", action="store")
parser.add_argument("-s", "--salvar", help="Nome do arquivo da imagem de saída.", action="store")
parser.add_argument("-a", "--analise", help="Modo de análise", action="store_true")
args = parser.parse_args()

steps = []

#Abre a imagem de entrada
input_filename = args.input
image = cv2.imread(input_filename, cv2.IMREAD_GRAYSCALE)
if args.analise:
    steps.append(cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB))

#Usa um filtro suavizador gaussiano para redução de ruídos  
image = cv2.GaussianBlur(image, (9,9), 2, 2)
if args.analise:
    steps.append(cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB))
    
#Detecta as bordas da imagem
edges = cv2.Canny(image, 120, 0, 5)   
if args.analise:
    image_with_edges = cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB)
    image_with_edges[edges==255] = [0, 0, 255];
    steps.append(image_with_edges)

#Aplica a transformada de Hough para detectar os círculos na imagem
circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 
                           1, 
                           minDist=image.shape[0]/100,
                           param2=120,
                           minRadius=0,
                           maxRadius=0
                           )

if args.analise:
    if circles is None:
        print "Nenhum círculo foi encontrado."
    else:
        print "Foram encontrados " + str(len(circles[0])) + " círculos."        
        image_with_circles = image
        #Desenha e imprime as informações dos círculos
        for i in range(0, len(circles[0])):
            print circles[0][i]
            center = (int(circles[0][i][0]), int(circles[0][i][1])) 
            cv2.circle(image_with_circles, center, 
                       int(circles[0][i][2]), (255, 0, 0), 3)
        steps.append(image_with_circles)
    
if args.analise:
    show_multiple_images(steps, "Passo a passo")
    
#Se especificado, salva a imagem de saída
if args.salvar != None:
    cv2.imwrite(args.salvar, image)