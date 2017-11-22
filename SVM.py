# -*- coding: utf-8 -*-
from sklearn import svm
import pickle
import numpy
import cv2
from conta_celulas import conta_celulas
from regiao import Regiao

def svm_cells(X, y):
    svm_linear = svm.SVC()
    svm_linear.fit(X, y)

    return svm_linear

def svm_predict(svm_cells, sample):
    return svm_cells.predict(sample)


def load_regioes_anotadas(file_name_pk):
    try:
        regioes_anotadas = pickle.load(open(file_name_pk,'rb'))
    except:
        regioes_anotadas = []
    X = []
    y = []
    for regiao in regioes_anotadas:
        X.append(regiao['caracteristicas'])
        y.append(regiao['classe'])
    X = numpy.array(X)
    y = numpy.array(y)
    return X, y

def classifica_imagem(svm, file_name):
    imagem = cv2.imread(file_name,cv2.IMREAD_COLOR)
    regioes_encontradas = conta_celulas(imagem=imagem)

    cv2.namedWindow('imagem', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('imagem', 600,600)

    for regiao_encontrada in regioes_encontradas:
        regiao = Regiao(regiao_encontrada)
        regiao.extrai_caracteristicas()

        X = [regiao.caracteristicas]

        classe = svm_predict(svm, X)[0]

        if classe == 'n':
            cv2.drawContours(imagem, regiao.get_contorno(), -1, (0,255,0), 6)
        elif classe == 'l':
            cv2.drawContours(imagem, regiao.get_contorno(), -1, (255,0,0), 6)
        else:
            cv2.drawContours(imagem, regiao.get_contorno(), -1, (0,0,255), 6)

    cv2.imshow('imagem', imagem)
    k = cv2.waitKey(0)

# X, y = load_regioes_anotadas('regioes_anotadas.p')
# svm = svm_cells(X, y)
# classifica_imagem(svm, "/home/nayara/Desktop/TCC/index_image/69.jpg")

# print(svm_predict(svm, sample))
