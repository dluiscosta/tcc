#gera as máscaras de cada lâmina anotada

import dill
dill.load_session(r'anotacoes_base\patchs.pkl')

shape = (4160, 3120) #tamanho das imagens

import numpy
import cv2
for i in range(1, 129):
    if laminas[i] is not None:
        mask = numpy.zeros(shape, dtype=numpy.uint8)
        cv2.circle(mask, laminas[i].centro, laminas[i].raio, 255, thickness=-1)
        cv2.imwrite("anotacoes_base\mascaras_laminas\\" + str(i) + ".png", mask)
