import pickle
with open("experimentos//remocao_ruidos01.pkl", "rb") as f:
    notas = pickle.load(f)
    f.close()
    
import numpy as np
import matplotlib.pyplot as plt
import math as mt

#Parametros variados
filtros = ["Sem filtro", "Filtro Media", "Filtro Mediana", "Filtro Gaussiano"]
tamanhos_kernels = [3, 5, 7, 9]
cores = ["blue", "green", "red", "gray"]
limiares = range(70, 241)

qtd_imagens = notas.shape[-1]

#Aplica a media no eixo das imagens
notas_medias = np.mean(notas, axis=4)

#Plota a nota media de cada limiar, um grafico para cada (filtro x tamanho_kernel)
for f, filtro in enumerate(filtros):
    #Figura para o filtro, com ao menos len(tamanhos_kernels) slots
    size = int(mt.sqrt(len(tamanhos_kernels)))
    fig, axes = plt.subplots(nrows=size, ncols=size)
    axes = np.ravel(axes) #1d array
    fig.suptitle(filtro)
    fig.tight_layout()
    
    for t, tamanho_kernel in enumerate(tamanhos_kernels):        
        #Prepara uma subfigura para um determinado tamanho de kernel
        ax = axes[t]
        ax.set_title("kernel (" + str(tamanho_kernel) + ", " + str(tamanho_kernel) + ")")
        ax.set_xlabel("limiares")
        ax.set_ylabel("indice de Jaccard medio")
        
        #Plota a curva correspondente a cada cor
        for c, cor in enumerate(cores):
            ax.plot(limiares, 1 - notas_medias[f, t, c], color = cor) 
            
        #Plota linha vertical no limiar otimo, na cor correspondente
        l_o, c_o = min([(l, c) for l,_ in enumerate(limiares) for c,_ in enumerate(cores)], #todas combinacoes (limiar x cor)
                       key = (lambda lc: notas_medias[f, t, lc[1], lc[0]])) #maxima nota media
        limiar_o = limiares[l_o]
        cor_o = cores[c_o]
        ax.axvline(limiar_o, color = cor_o)
        
        print (limiar_o, cor_o, notas_medias[f, t, c_o, l_o])
        
        '''
        ax.text(limiar_o, 5, "limiar otimo", rotation=90, verticalalignment="center")
        plt.text(limiar_o, 0, str(limiar_o), rotation=45, verticalalignment="bottom")
        plt.text(limiar_o, notas_medias[l_o, c_o], str(notas_medias[l_o, c_o]), rotation=45)
        '''
    plt.show()
    
    
    
#Plota a melhor nota (limiar x cor otima), media e desvio padrao entre imagens, p/ cada (filtro x tamanho_kernel)
notas_min = np.min(notas, axis=3) #busca o melhor desempenho pelos limiares
notas_min = np.min(notas_min, axis=2) #e pelas cores
notas_min_medias = np.mean(notas_min, axis=2) #calcula a media entre as imagens

fig = plt.figure()
fig.suptitle("Melhor desempenho medio alcancado por limiarizacao")
plt.xlabel("tamanho do kernel")
plt.ylabel("melhor indice de Jaccard")       
for f,filtro in enumerate(filtros):
    plt.scatter(tamanhos_kernels, 1 - notas_min_medias[f], label=filtro)
plt.legend(loc="best")
plt.show()