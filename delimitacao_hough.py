import cv2
import cv2.cv
import argparse
from exibir_imagens import show_multiple_images 

#Parser de parâmetros do script
parser = argparse.ArgumentParser(description="Delimita a região circular da lâmina.")
parser.add_argument("input", help="Nome do arquivo da imagem de entrada.", action="store")
parser.add_argument("-s", "--salvar", help="Nome do arquivo da imagem de saída.", action="store")
parser.add_argument("-a", "--analise", help="Modo de análise", action="store_true")
args = parser.parse_args()


#Imagens a serem exibidas
steps = []


#Abre a imagem de entrada
input_filename = args.input
image = cv2.imread(input_filename, cv2.IMREAD_GRAYSCALE)

if args.analise:
    steps.append(cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB))



#Usa um filtro suavizador gaussiano para redução de ruídos  
image = cv2.GaussianBlur(image, (13,13), 2, 2)

if args.analise:
    steps.append(cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB))

    
#Detecta as bordas da imagem
edges = cv2.Canny(image, 80, 0, apertureSize = 3)   

if args.analise:
    image_with_edges = cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB)
    image_with_edges[edges==255] = [0, 0, 255];
    steps.append(image_with_edges)


#Aplica a transformada de Hough para detectar os círculos na imagem
circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 
                           1, 
                           minDist=image.shape[0]/100,
                           param2=80,
                           minRadius=0,
                           maxRadius=0
                           )

if args.analise:
    if circles is None:
        print "Nenhum círculo foi encontrado."
    else:
        print "Foram encontrados " + str(len(circles[0])) + " círculos."        
        image_with_circles = cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB)
        #Desenha e imprime as informações dos círculos
        for i in range(0, len(circles[0])):
            print circles[0][i]
            center = (int(circles[0][i][0]), int(circles[0][i][1])) 
            cv2.circle(image_with_circles, center, 
                       int(circles[0][i][2]), (255, 0, 0), 3)
        steps.append(image_with_circles)


#Exibe os passos do procedimento
if args.analise:
    show_multiple_images(steps, "Passo a passo")

    
#Se especificado, salva a imagem de saída
if args.salvar != None:
    cv2.imwrite(args.salvar, image)