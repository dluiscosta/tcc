from remocao_ruidos import filtro_media, filtro_mediana, filtro_gaussiano
import base
import cv2
import numpy as np

#Parametros variados
filtros = [lambda im, ks: im, filtro_media, filtro_mediana, filtro_gaussiano]
tamanhos_kernels = [3, 5, 7, 9]
cores = [0, 1, 2, 3]
limiares = range(70, 241)
imagens = base.base.get_imagens(lambda im:im.lamina is not None #lamina anotada
                                and im.get_patch().celulas is not None) #celulas anotadas

notas = np.zeros(shape=(len(filtros), len(tamanhos_kernels), len(cores), len(limiares), len(imagens)),
                 dtype=float)

for i in range(len(imagens)):
    imagem = imagens[i]
    im_total = imagem.get_imagem() #carrega a imagem
    patch = imagem.get_patch()
    
    for c in range(len(cores)):
        #Pega a imagem na cor escolhida
        cor = cores[c]
        im_cor = None
        if cor < 3:
            im_cor = im_total[:,:,cor]
        else:
            im_cor = cv2.cvtColor(im_total, cv2.cv.CV_BGR2GRAY)
        
        for f in range(len(filtros)):
            filtro = filtros[f]
            for t in range(len(tamanhos_kernels)):
                tamanho_kernel = tamanhos_kernels[t]
                
                #Aplica o filtro sobre a imagem completa para nao haver prejuizo nas extremidades do patch
                im_filt = filtro(im_cor, tamanho_kernel)
                x, y = patch.canto
                h, w = base.shape_patch
                im_patch = im_filt[y:y+h, x:x+h]
                
                for l in range(len(limiares)):
                    #Aplica o limiar e salva a distancia de jaccard para com o padrao ouro
                    limiar = limiares[l]
                    im_bin = cv2.threshold(im_patch, limiar, 255, cv2.THRESH_BINARY_INV)[1]
                    notas[f, t, c, l, i] = patch.avaliacao_distancia_jaccard(im_bin)
                    
                    print (f, tamanho_kernel, cor, limiar, i, notas[f, t, c, l, i])
                
import pickle
with open("experimentos/remocao_ruidos01.pkl", "wb") as f:
    pickle.dump(notas, f)
    f.close()