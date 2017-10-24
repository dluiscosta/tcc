#Calcula o desempenho da limiarizacao por otsu

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

cores = range(cores)

#Carrega as imagens
import base
ims = base.base.get_imagens(lambda im:im.lamina is not None and im.get_patch().celulas is not None)
patchs = map(lambda im: im.get_patch(), ims)
patchs_ims = map(lambda pt: pt.get_imagem(), patchs)

#Computa as imagens em cada cor
ims_cor = ([[patch_im[:,:,cor] for patch_im in patchs_ims] for cor in cores[:-1]] + 
           [map(lambda im: cv2.cvtColor(im, cv2.cv.CV_BGR2GRAY), patchs_ims)])

#Calcula a media de desempenho da limiarizacao por otsu para cada (cor, c, gamma)
def otsu_mean(cor):
    #Computa os limiares retornados pela ldf (com c e gamma), para cada imagem
    limiares = [cv2.threshold(im, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[0] for im in ims_cor[cor]]

    #Consulta a nota da limiarizacao pelo limiar computado, para cada imagem, e tira a media
    nota_media = np.mean([notas_norm[int(limiares[im_idx]), cor, im_idx] for im_idx in range(imagens)]) #mesmo limiar
    nota_media_div2 = np.mean([notas_norm[int(limiares[im_idx]/2), cor, im_idx] for im_idx in range(imagens)]) #metade limiar
    
    print (cor, nota_media, nota_media_div2)
    return (nota_media, nota_media_div2)

notas_ldf = [otsu_mean(cor) for cor in cores]

#Salva os resultados
with open("experimentos//seg_otsu01.pkl", "wb") as f:
    parametros = (cores)
    pickle.dump((parametros, notas_ldf), f)
    f.close()


