#Para as imagens com as celulas anotadas, apos aplicacao do filtro de mediana (tamanho kernel variavel), 
#checa no patch a qualidade da segmentacao por limiarizacao nos limiares 146(que o de maior indice de Jaccard medio) +- 5 
#sobre o canal verde, apos extracao de regioes com variacao nos kerneis das aberturas morfologicas.

import base
import cv2
import numpy as np
import pickle
from remocao_ruidos import filtro_mediana
from extrair_regioes import extrair_regioes

#Parametros variaveis
kernels_filt_med = [5, 7, 9] #tamanhos do kernel do filtro de mediana 
limiares = range(146-10, 146+10+1)
imagens = base.base.get_imagens(lambda im:im.lamina is not None and im.get_patch().celulas is not None)

#Define os kerneis de abertura (variavel)
morphs = [cv2.MORPH_CROSS, cv2.MORPH_RECT, cv2.MORPH_ELLIPSE]
kernels_ext = [None] + [cv2.getStructuringElement(morph, (ksize, ksize)) 
               for ksize in range(3, 8, 2) for morph in morphs]
kernels_int = [None]
# + [cv2.getStructuringElement(morph, (ksize, ksize)) 
#               for ksize in range(3, 6, 2) for morph in morphs]
#areas_min = range(500, 1000, 100)

notas = np.zeros((len(kernels_filt_med),
                  len(kernels_ext),
                  len(kernels_int),
                  #len(areas_min),
                  len(limiares),
                  len(imagens)),dtype=float)

for i, imagem in enumerate(imagens): #para cada imagem
    patch = imagem.get_patch()
    im_g = imagem.get_imagem()[:,:,1] #pega apenas o canal verde
    
    for kf,kernel_filt_med in enumerate(kernels_filt_med):
        im_f = filtro_mediana(im_g, kernel_filt_med) #aplica o filtro de mediana
        x, y = patch.canto
        h, w = base.shape_patch
        im_p = im_f[y:y+h, x:x+w] #pega apenas a regiao do patch
            
        for l, limiar in enumerate(limiares):
            im_b = cv2.threshold(im_p, limiar, 255, cv2.THRESH_BINARY_INV)[1] #limiariza
            
            for ke, kernel_ext in enumerate(kernels_ext): #para cada kernel externo
                for ki, kernel_int in enumerate(kernels_int): #para cada kernel interno
                    #for a, area_min in enumerate(areas_min): #para cada area minima
                    regioes = extrair_regioes(im_b, kernel_ext, kernel_int) #extrai as regioes
                        
                    #Calcula a media de, para cada celula, a distancia de Jaccard para com a regiao mais semelhante 
                    notas[kf,ke,ki,l,i] = patch.avaliacao_forca_bruta(regioes, base.distancia_jaccard, ignora_borda=True)
                       
                    print(kf,ke,ki,limiar,imagem.indice,notas[kf,ke,ki,l,i])
            
    with open("experimentos//extrair_regioes02.pkl", "wb") as f:
        pickle.dump(notas, f)
        f.close()