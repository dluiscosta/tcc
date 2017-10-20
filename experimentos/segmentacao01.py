#Para as imagens com as celulas anotadas, checa no patch a qualidade da segmentacao por
#limiarizacao com cada limiar (passo 10)

import base
import cv2
import numpy as np
import pickle

limiares = range(0, 255)
cores = (0, 1, 2, 3)
ims = base.base.get_imagens(lambda im:im.lamina is not None and im.get_patch().celulas is not None)

notas = np.zeros((len(limiares),
                  len(cores),
                  len(ims)),dtype=int)

with open("..//..//..//Dropbox//segmentacao01.pkl", "wb") as f:
    pickle.dump(notas, f)
    f.close()
        
for i in range(len(ims)):
    im = ims[i]
    patch = im.get_patch()
    original = patch.get_imagem()
    
    for c in range(len(cores)):
        cor = cores[c]
        if cor == 3:
            imagem = cv2.cvtColor(original, cv2.cv.CV_BGR2GRAY)
        else:
            imagem = original[:,:,cor]
            
        for l in range(len(limiares)):
            limiar = limiares[l]
            binaria = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY_INV)[1]    
            tentativa = cv2.findContours(binaria, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
            nota = patch.avaliar_patch(tentativa, analise=False)
            
            print (im.indice, cor, limiar, nota)
            notas[l,c,i] = nota
            
    with open("experimentos//segmentacao01.pkl", "wb") as f:
        pickle.dump(notas, f)
        f.close()