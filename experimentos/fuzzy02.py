import pickle
with open("experimentos//remocao_ruidos01.pkl", "rb") as f:
    notas = pickle.load(f)
    f.close()
    
import numpy as np
import cv2

#filtros = ["Sem filtro", "Filtro Media", "Filtro Mediana", "Filtro Gaussiano"]
#tamanhos_kernels = [3, 5, 7, 9]
#cores = ["blue", "green", "red", "gray"]
#limiares = range(70, 241)

notas = notas[2,3] #Apenas filtro de mediana, tamanho 9x9

##Parametros variados
cores = ["blue", "green", "red", "gray"]
cs = np.linspace(start=1/float(256), stop=5, num=20)
gammas = np.linspace(start=1, stop=400, num=30)

#Carrega as imagens
import base
ims = base.base.get_imagens(lambda im:im.lamina is not None and im.get_patch().celulas is not None)
patchs = map(lambda im: im.get_patch(), ims)
patchs_ims = map(lambda pt: pt.get_imagem(), patchs)

#Aplica o filtro de mediana nas imagens
from remocao_ruidos import remocao_ruidos as rr
patchs_filt = [rr(im) for im in patchs_ims]

#Separa as cores
ims_cor = ([[im[:,:,c] for im in patchs_filt] for c,cor in enumerate(cores[:-1])] + 
           [map(lambda im: cv2.cvtColor(im, cv2.cv.CV_BGR2GRAY), patchs_filt)])


#Calcula o limiar da divergência fuzzy sobre cada imagem em cada cor

from limiarizacao_divergencia_fuzzy import limiarizacao_divergencia_fuzzy as ldf
def get_ldf(im, c, gamma, cor):
    limiar = ldf(im, c=c, gamma=gamma)[0]
    print (c, gamma, cor, limiar)
    return limiar

limiares = [[[[
            get_ldf(im, c, gamma, cor)
            for im in ims_cor[cor_idx]]
            for gamma in gammas]
            for c in cs]
            for cor_idx,cor in enumerate(cores)]
limiares = np.array(limiares)

#Salva os resultados
with open("experimentos//fuzzy02.pkl", "wb") as f:
    parametros = (cores, cs, gammas, [im.indice for im in ims])
    pickle.dump((parametros, limiares), f)
    f.close()
    
#Consulta a nota atribuida a segmentacao resultado do limiar do ldf e da metade

def get_nota(cor_idx, i, l):
    if l < 70 or l > 240:
        return 1 #distancia maxima
    else:
        return notas[cor_idx, l-70, i]
    
notas_ldf = [[[[
            (get_nota(cor_idx, i, limiares[cor_idx, c_idx, g, i]), #nota no limiar da ldf
             get_nota(cor_idx, i, limiares[cor_idx, c_idx, g, i]/2)) #nota no limiar/2
            for i,im in enumerate(ims_cor[cor_idx])]
            for g,gamma in enumerate(gammas)]
            for c_idx,c in enumerate(cs)]
            for cor_idx,cor in enumerate(cores)]
notas_ldf = np.array(notas_ldf)

#Salva os resultados
with open("experimentos//fuzzy02.pkl", "wb") as f:
    parametros = (cores, cs, gammas, [im.indice for im in ims])
    pickle.dump((parametros, limiares, notas_ldf), f)
    f.close()