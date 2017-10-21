import pickle
with open("experimentos//segmentacao01.pkl", "rb") as f:
    notas = pickle.load(f)
    f.close()
    
import numpy as np
import matplotlib.pyplot as plt

limiares, cores, imagens = notas.shape
notas_swap = np.swapaxes(notas, 0, 2) #inverte a ordem das dimensoes de limiares e imagens

#Computa o melhor limiar para cada (imagem, cor)
l_otms = np.zeros((cores, imagens), dtype=np.uint8)
for c in range(cores): #para cada cor
    def limiar_otimo(notas):
        return min(range(limiares), key=(lambda l: notas[l]))
    
    l_otms[c] = map(limiar_otimo, notas_swap[:, c, :]) #para todas imagens, computa o limiar otimo
    #Mostra o histograma de melhores limiares para aquela cor
    plt.hist(l_otms[c], bins=25)
    plt.show()
    
#Computa o melhor (limiar, cor) para cada imagem
lc_otms = np.zeros((imagens,), dtype=(np.uint8, np.uint8))
def lc_otimos(notas):
    return min([(l,c) for l in limiares for c in cores], key=(lambda l, c: notas[c, l]))
lc_otms = map(lc_otimos, notas_swap)

#Mostra o histograma de melhores (limiar, cor)
lc_otms2 = [[l for (l, c) in lc_otms if c == c2] for c2 in range(cores)]
plt.hist(lc_otms2, bins=25, color = ['b', 'g', 'r', "gray"], stacked=True, rwidth=0.9)
plt.show()
    
    
#Normaliza as notas, dividindo pela diferenca maxima (soma das areas das celulas) e invertendo na soma
notas_norm_swap = map(lambda v: v.astype(float)/float(max([np.max(v), 1])), notas_swap)
notas_norm_swap = 1 - np.array(notas_norm_swap)
notas_norm = np.swapaxes(notas_norm_swap, 0, 2) #inverte a ordem das dimensoes de limiares e imagens

#Aplica a media no eixo das imagens
notas_media = np.mean(notas_norm, axis=2)

#Plota uma curva para cada cor com o desempenho em funcao do limiar
for c in range(cores):
    plt.plot(range(limiares), notas_media[:, c], color = ['b', 'g', 'r', "gray"][c]) 
l, c = max([(l,c) for l in limiares for c in cores], #computa o (limiar, cor) otimo
           key = (lambda l, c: notas_media[l, c]))
plt.axvline(l, color = ['b', 'g', 'r', "gray"][c]) #traca linha vertical no limiar otimo da melhor cor
plt.show()