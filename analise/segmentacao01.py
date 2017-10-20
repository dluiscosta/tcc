import pickle
with open("experimentos//segmentacao01.pkl", "rb") as f:
    notas = pickle.load(f)
    f.close()
    
import numpy as np
import matplotlib.pyplot as plt
import itertools

limiares, cores, imagens = notas.shape
notas_swap = np.swapaxes(notas, 0, 2) #inverte a ordem das dimensoes de limiares e imagens
    
for c in range(cores): #para cada cor
    def limiar_otimo(notas):
        return min(range(limiares), key=(lambda l: notas[l]))
    
    l_otms = map(limiar_otimo, notas_swap[:, c, :]) #para todas imagens, computa o limiar otimo
    print l_otms
    #printa histograma
    
#Normaliza as notas, dividindo pela diferenca maxima (soma das areas das celulas) e invertendo na soma
notas_norm_swap = map(lambda v: v.astype(float)/float(max([np.max(v), 1])), notas_swap)
notas_norm_swap = 1 - np.array(notas_norm_swap)
notas_norm = np.swapaxes(notas_norm_swap, 0, 2) #inverte a ordem das dimensoes de limiares e imagens

#Aplica a media no eixo das imagens
notas_media = np.mean(notas_norm, axis=2)

for c in range(cores):
    plt.plot(range(limiares), notas_media[:, c], color = ['b', 'g', 'r', "gray"][c]) 
l, c = max(list(itertools.product(range(limiares), range(cores))),
           lambda lc: notas_media[lc[0], lc[1]])
plt.axvline(l, color=c)
plt.show()