import base
import cv2
import numpy as np
import pickle
import matplotlib.pyplot as plt

with open("experimentos//extrair_regioes02.pkl", "rb") as f:
    notas = pickle.load(f)
    f.close()

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


morphs_nome = ["Cruz", "Retangulo", "Elipse"]
nomes_ker = ["Sem abertura"] + [morph + " " + str(ksize) + "x" + str(ksize)
             for ksize in range(3, 8, 2) for morph in morphs_nome]

   
for kf,kernel_filt_med in enumerate(kernels_filt_med):
    fig = plt.figure()
    fig.suptitle(kernel_filt_med)
    plt.xlabel("limiar")
    plt.ylabel("indice de Jaccard medio")    
        
    for ke, kernel_ext in enumerate(kernels_ext): #para cada kernel externo
  
    
        for ki, kernel_int in enumerate(kernels_int): #para cada kernel interno
            #Calcula, por limiar, a media entre as 30 imagens.
            notas_lim = np.mean(notas[kf, ke, ki], axis=1)
            plt.scatter(limiares, 1-notas_lim, label=nomes_ker[ke])
            
    plt.legend(loc="best")
    plt.show()
            