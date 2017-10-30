#Varia os os parametros da delimitacao_otsu e avalia a saida usando a
#metrica da distancia de Jaccard, comparando a mascara produzida com a lamina anotada.

import base
from delimitacao_otsu import delimitacao_otsu
import numpy as np
import cv2

imagens = base.base.get_imagens(lambda im: im.lamina is not None)

#Parametros variados
cores = ["blue", "green", "red", "grey"] #BGR e cinza
rem_reg_esp = [True, False] #remocao de regioes espurias 
#(eh mantida a com maior area e removidas as demais)
enc_circ = [True, False] #encaixe de um circulo

shape = (len(cores), #cores
         len(rem_reg_esp), 
         len(enc_circ), 
         len(imagens))
notas = np.zeros(shape, dtype=float)

for i, imagem in enumerate(imagens): #para cada imagem
    im_ori = imagem.get_imagem()
    im_lam = imagem.lamina.get_imagem() #lamina anotadas
    for c, cor in enumerate(cores): #em cada canal de cor e nos tons de cinza
        im_cor = im_ori[:,:,c] if cor != "grey" else cv2.cvtColor(im_ori, cv2.cv.CV_BGR2GRAY)
        
        #Conduz a delimitacao da lamina limiarizando por otsu.
        #Varia os dois parametros da delimitacao_otsu. 
        for r, rem in enumerate(rem_reg_esp):
            for e, enc in enumerate(enc_circ):
                im_otsu = delimitacao_otsu(im_cor, analise=False,
                                        removeEspurias=rem,
                                        encaixaCirculo=enc)
                #Armazena a distancia de jaccard da mascara computada para com a anotada.
                notas[c,r,e,i] = base.distancia_jaccard(im_lam, im_otsu)
                
                print(cor,rem,enc,i,notas[c,r,e,i])

import pickle
with open("experimentos//delimitacao02.pkl", "wb") as f:
    pickle.dump(notas, f)
    f.close()