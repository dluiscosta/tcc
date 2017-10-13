import base
from delimitacao_otsu import delimitacao_otsu
import numpy as np

cores = ["azul", "verde", "vermelho"]
for c in [0, 1, 2]: #canais BGR
    notas = []
    for im in base.base.get_imagens(lambda im: im.lamina is not None):
        imagem = im.get_imagem()[:,:,c]
        otsu = delimitacao_otsu(imagem)
        notas.append(im.lamina.avaliar_lamina(otsu, analise=False, indice=im.indice))
    media = np.mean(notas)
    print "Cor " + str(cores[c]) + ": " + str(media)