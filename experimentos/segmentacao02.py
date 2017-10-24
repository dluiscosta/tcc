#Para as imagens com as celulas anotadas, checa no patch a qualidade da segmentacao por
#limiarizacao com cada limiar sobre a imagem filtrada com o filtro da mediana 5x5

import base
import cv2
import numpy as np
import pickle

limiares = range(0, 255)
cores = (0, 1, 2, 3, 4, 5, 6) #RGB com o filtro aplicado antes da separação, cinza, RGB com o filtro aplicado depois da separação
ims = base.base.get_imagens(lambda im:im.lamina is not None and im.get_patch().celulas is not None)

notas = np.zeros((len(limiares),
                  len(cores),
                  len(ims)),dtype=int)
        


for i in range(len(ims)):
    im = ims[i]
    patch = im.get_patch()
    original = patch.get_imagem()
    
    for c in range(len(cores)):
        cor = cores[c]
        if cor == 3:
            imagem = cv2.cvtColor(original, cv2.cv.CV_BGR2GRAY)
        elif cor < 3:
            imagem = cv2.medianBlur(original, ksize=5)[:,:,cor]
        else:
            imagem = cv2.medianBlur(original[:,:,cor-4], ksize=5)
            
        for l in range(len(limiares)):
            limiar = limiares[l]
            binaria = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY_INV)[1]    
            tentativa = cv2.findContours(binaria, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
            nota = patch.avaliar_patch(tentativa, analise=False)
            
            print (im.indice, cor, limiar, nota)
            notas[l,c,i] = nota
            
    with open("experimentos//segmentacao02.pkl", "wb") as f:
        pickle.dump(notas, f)
        f.close()