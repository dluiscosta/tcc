#Calcula o desempenho da limiarizacao por divergencia fuzzy, variando os parametros c e gamma.

import pickle
with open("experimentos//segmentacao01.pkl", "rb") as f:
    notas = pickle.load(f)
    f.close()
    
import numpy as np
import cv2

limiares, cores, imagens = notas.shape
notas_swap = np.swapaxes(notas, 0, 2) #inverte a ordem das dimensoes de limiares e imagens

#Normaliza as notas, dividindo pela diferenca maxima (soma das areas das celulas) e invertendo na soma
notas_swap = np.swapaxes(notas, 0, 2) #inverte a ordem das dimensoes de limiares e imagens
notas_norm_swap = map(lambda v: v.astype(float)/float(max([np.max(v), 1])), notas_swap)
notas_norm_swap = 1 - np.array(notas_norm_swap)
notas_norm = np.swapaxes(notas_norm_swap, 0, 2) #inverte a ordem das dimensoes de limiares e imagens

#Parametros que serao testados, com os eixos nesta ordem
cores = range(cores)
cs = np.linspace(start=1/float(256), stop=5, num=20)
gammas = np.linspace(start=1, stop=400, num=30)

#Carrega as imagens
import base
ims = base.base.get_imagens(lambda im:im.lamina is not None and im.get_patch().celulas is not None)
patchs = map(lambda im: im.get_patch(), ims)
patchs_ims = map(lambda pt: pt.get_imagem(), patchs)

#Computa as imagens em cada
ims_cor = ([[patch_im[:,:,cor] for patch_im in patchs_ims] for cor in cores[:-1]] + 
           [map(lambda im: cv2.cvtColor(im, cv2.cv.CV_BGR2GRAY), patchs_ims)])

#Calcula a media de desempenho da limiarizacao por divergencia fuzzy para cada (cor, c, gamma)
from limiarizacao_divergencia_fuzzy import limiarizacao_divergencia_fuzzy as ldf
def ldf_mean(cor, c, gamma):
    #Computa os limiares retornados pela ldf (com c e gamma), para cada imagem
    limiares_ldf = [ldf(im, c=c, gamma=gamma)[0] for im in ims_cor[cor]]
    #Consulta a nota da limiarizacao pelo limiar computado, para cada imagem, e tira a media
    nota_media = np.mean([notas_norm[limiares_ldf[im_idx], cor, im_idx] for im_idx in range(imagens)]) #mesmo limiar
    nota_media_div2 = np.mean([notas_norm[int(limiares_ldf[im_idx]/2), cor, im_idx] for im_idx in range(imagens)]) #metade limiar
    
    print (cor, c, gamma, nota_media, nota_media_div2)
    return (nota_media, nota_media_div2)

notas_ldf = [[[ldf_mean(cor, c, g) for g in gammas] for c in cs] for cor in cores]

#Salva os resultados
with open("experimentos//fuzzy01.pkl", "wb") as f:
    parametros = (cores, cs, gammas)
    pickle.dump((parametros, notas_ldf), f)
    f.close()
