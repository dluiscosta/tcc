import base
from delimitacao_otsu import delimitacao_otsu
import numpy as np
import cv2

imagens = base.base.get_imagens(lambda im: im.lamina is not None and (im.indice == 5 or im.indice == 111))

cores = ["azul", "verde", "vermelho", "cinza"]
shape = (4, #cores
         2, #remocao de regioes espurias
         2, #encaixe de um circulo
         len(imagens))
notas = np.zeros(shape,dtype=float)

for i in range(0, len(imagens)):
    im = imagens[i]
    original = im.get_imagem()
    for c in [0, 1, 2, 3]:  #canais BGR e tons de cinza
        if c == 3:
            imagem = cv2.cvtColor(original, cv2.cv.CV_BGR2GRAY)
        else:
            imagem = original[:,:,c]
        for re in [True, False]:
            for ec in [True, False]:
                otsu = delimitacao_otsu(imagem, analise=False,
                                        removeEspurias=re,
                                        encaixaCirculo=ec)
                notas[c,int(re),int(ec),i] = im.lamina.avaliar_lamina(otsu, analise=False)

maior_media = 0
prep = ["sem", "com"]
for c in [0, 1, 2, 3]: 
    for re in [0, 1]:
        for ec in [0, 1]:
            media = np.mean(notas[c,re,ec,:])
            if media > maior_media:
                maior_media = media
                par_ot = (c, re, ec)
            print ("Cor " + cores[c] +
                   ", " + prep[re] + " remocao de regioes espurias" +
                   ", " + prep[ec] + " encaixe de circulo" +
                   ": " + str(media))
            
print "MELHOR MEDIA: " + str(maior_media)
print ("Cor " + cores[par_ot[0]] +
       ", " + prep[par_ot[1]] + " remocao de regioes espurias" +
       ", " + prep[par_ot[2]] + " encaixe de circulo" +
       ".")