import cv2
import cv2.cv
import argparse
from exibir_imagens import mostra_imagens
import numpy as np
import random as rd

#Gera cor aleatoria com saturacao e valor maximo (bem visivel), apenas alterando o hue.
def cor_aleatoria(minHue=0, maxHue=180):
    c = np.zeros((1, 1, 3), dtype=np.uint8) #imagem para conversao
    c[0][0] = [rd.randint(minHue, maxHue), 100, 100] #cor aleatoria em HSV
    c = cv2.cvtColor(c, cv2.COLOR_HSV2BGR) #converte para BGR   
    cor = c[0][0]    
    return np.array([int(cor[0]), int(cor[1]), int(cor[2])])   

#Extrai os componentes conexos (em contornos) de uma imagem binaria.
#Se especificados kerneis, aplica uma abertura sobre os componentes (contornos externos) 
#e uma abertura sobre os buracos (contornos internos).
#Se fornecida uma area minima, elimina as regioes que nao satisfizerem essa condicao.    
def extrair_regioes(imagem, kernel_ext=None, kernel_int=None, min_area=None, analise=False, original=None):
    if analise:
        mostra_imagens([imagem], "", ["Imagem de entrada, apenas um canal"])
        
    #Encontra os contornos das regioes
    contours, hierarchy = cv2.findContours(np.copy(imagem), 
            cv2.RETR_CCOMP, #associa contornos de componentes com contornos de buracos
            cv2.CHAIN_APPROX_NONE) #armazena todos os pontos no contorno
    
    #Aplica as aberturas
    if kernel_int is not None or kernel_ext is not None:
        #Separa os componentes (contornos externos) e os buracos em 2 imagens
        im_ext, im_bur = np.zeros((2,) + imagem.shape, dtype=np.uint8)
        for c,cont in enumerate(contours):
            if hierarchy[0,c,3] == -1: #nao tem pai -> eh componente
                cv2.drawContours(im_ext, [cont], -1, [255], -1)
                cv2.drawContours(im_ext, [cont], -1, [255], 1)
            else:
                cv2.drawContours(im_bur, [cont], -1, [255], -1)
                cv2.drawContours(im_bur, [cont], -1, [255], 1)
        if analise:
            mostra_imagens([im_ext, im_bur], "Componentes e buracos separados")
            
        #Aplica uma abertura nos componentes externos para separar as celulas grudadas
        if kernel_ext is not None:
            im_ext = cv2.morphologyEx(im_ext, cv2.MORPH_OPEN, kernel_ext)
        
        #Aplica uma abertura nos buracos para remover espurios e suavizar o formato
        if kernel_int is not None:
            im_bur = cv2.morphologyEx(im_bur, cv2.MORPH_OPEN, kernel_int)
        
        if analise and (kernel_ext is not None or kernel_int is not None):
            mostra_imagens([im_ext, im_bur], "Componentes e buracos abertos")
            
        #Desenha os buracos sobre a imagem com os componentes abertos e retira os contornos novamente
        im_ab = np.copy(im_ext)
        im_ab[im_bur == 255] = 0
            
        if analise:
            mostra_imagens([im_ab], "Regioes apos abertura")
        
        #Extrai os contornos atualizados
        contours, hierarchy = cv2.findContours(im_ab, 
            cv2.RETR_CCOMP, #associa contornos de componentes com contornos de buracos
            cv2.CHAIN_APPROX_NONE) #armazena todos os pontos no contorno                   
    
    #Remove as regioes inferiores a min_area
    if min_area is not None:
        from extracao_caracteristicas import area
        im_area = np.zeros(imagem.shape, dtype=np.uint8)
        
        #Desenha as regioes superiores a min_area
        for c,cont in enumerate(contours):
            if hierarchy[0,c,3] == -1: #nao tem pai -> eh componente
            
                #Concatena o contorno do componente e dos buracos
                conts = [cont]
                if hierarchy[0,c,2] != -1: #ha filho(s) -> buracos
                    c_filho = hierarchy[0,c,2] #primeiro filho
                    conts.append(contours[c_filho])
                    while hierarchy[0,c_filho,0] != -1: #itera pelos outros filhos
                        c_filho = hierarchy[0,c_filho,0]
                        conts.append(contours[c_filho])
                        
                #Desenha se a regiao for superior a min_area
                if area(conts) >= min_area: #checa a area
                    cv2.drawContours(im_area, conts[:1], -1, [255], -1)
                    cv2.drawContours(im_area, conts[:1], -1, [255], 1)
                    cv2.drawContours(im_area, conts[1:], -1, [0], -1)
                    cv2.drawContours(im_area, conts[1:], -1, [0], 1)
                
        if analise:
            mostra_imagens([im_area], "Apenas regioes superiores a area minima")                
                
        #Extrai os contornos atualizados
        contours, hierarchy = cv2.findContours(im_area, 
            cv2.RETR_CCOMP, #associa contornos de componentes com contornos de buracos
            cv2.CHAIN_APPROX_NONE) #armazena todos os pontos no contorno                   
    
                    
        if original is not None:
            #Desenha os contornos obtidos sobre a imagem original
            im_cont = np.copy(original)
            for c, contorno in enumerate(contours):
                cor = cor_aleatoria()
        
                #So desenha o contorno se ele nao for filho de outro contorno.
                #Nesse caso, o contorno sera desenhado na vez do seu pai, 
                #com a mesma cor que ele
                if hierarchy[0,c,3] == -1: #nao tem pai
                    cv2.drawContours(im_cont, [contorno], -1, cor, 2)   
                    #Se houverem filhos, os desenha.
                    if hierarchy[0,c,2] != -1: #ha filho(s)
                        c_filho = hierarchy[0,c,2] #primeiro filho
                        cv2.drawContours(im_cont, contours, c_filho, cor, 2)  
                        while hierarchy[0,c_filho,0] != -1: #itera pelos outros filhos
                            c_filho = hierarchy[0,c_filho,0]
                            cv2.drawContours(im_cont, contours, c_filho, cor, 2)  
            if analise:
                mostra_imagens([im_cont], "Regioes encontradas sobre a imagem original")
       
    return contours, hierarchy
                        
#Parser de parametros do script
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

