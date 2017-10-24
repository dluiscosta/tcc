# -*- coding: utf-8 -*-

import pickle
with open("experimentos//fuzzy01.pkl", "rb") as f:
    parametros, notas = pickle.load(f)
    f.close()
    

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

notas = np.array(notas)

#Parametros que variam, eixos nesta ordem:
cores, cs, gammas = parametros

#Separa as notas para cada segmentacao, com o limiar otimo e com metade dele
seg, seg_div2 = (notas[:,:,:,0], notas[:,:,:,1])

#Mostra graficos das notas com uma superfície por cor, sobrepostas.
x, y = np.meshgrid(cs, gammas)

def plota(z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for cor in cores:
        ax.plot_surface(x, y, np.transpose(z[cor]), #plota a superficie
                        color=['b', 'g', 'r', "gray"][cor], alpha=0.5)
        
    cor_max, c_max, gamma_max = np.unravel_index(np.argmax(z), z.shape) #encontra o maximo (indices)
    maximo = (x[gamma_max, c_max], y[gamma_max, c_max], z[cor_max].max()) #passa para coordenadas do grafico
    ax.plot(*map(lambda x: [x], maximo), marker="o", ls="", #plota o ponto maximo
             color=['b', 'g', 'r', "gray"][cor_max])
    plt.show()

plota(seg) #para a segmentacao com o limiar otimo
plota(seg_div2) #para a segmentacao com a metade do limiar otimo