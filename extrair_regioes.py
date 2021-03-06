import cv2
import cv2.cv
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
    
    #Separa as regioes (cada regiao = 1 contorno externo + n contornos internos )
    regioes = [] #lista de regioes
    for c, contorno in enumerate(contours):
        #Monta uma regiao para cada contorno externo (primeiro nivel hierarquico)
        if hierarchy[0,c,3] == -1: #nao tem pai -> eh externo
            regiao = [contorno]
            #Se houverem filhos, os inclue.
            if hierarchy[0,c,2] != -1: #ha filho(s)
                c_filho = hierarchy[0,c,2] #primeiro filho
                regiao.append(contours[c_filho])
                while hierarchy[0,c_filho,0] != -1: #itera pelos outros filhos
                    c_filho = hierarchy[0,c_filho,0]
                    regiao.append(contours[c_filho])
            #Adiciona a regiao recem criada a lista de todas as regioes
            regioes.append(regiao)
                    
    #Remove as regioes inferiores a min_area
    if min_area is not None:
        from extracao_caracteristicas import area
        regioes = [r for r in regioes if area(r) >= min_area]
        
        if analise:
            #Desenha apenas as regioes superiores a min_area
            im_area = np.zeros(imagem.shape, dtype=np.uint8)
            for regiao in regioes:
                cv2.drawContours(im_area, regiao[:1], -1, [255], -1)
                cv2.drawContours(im_area, regiao[:1], -1, [255], 1)
                cv2.drawContours(im_area, regiao[1:], -1, [0], -1)
                cv2.drawContours(im_area, regiao[1:], -1, [0], 1)
            mostra_imagens([im_area], "Apenas regioes superiores a area minima")   

    if original is not None and analise:
        #Desenha os contornos obtidos sobre a imagem original
        im_cont = np.copy(original)
        for regiao in regioes:
            cv2.drawContours(im_cont, regiao, -1, cor_aleatoria(), 2)
        mostra_imagens([im_cont], "Regioes encontradas sobre a imagem original")
       
    return regioes