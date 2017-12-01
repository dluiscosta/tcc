# -*- coding: utf-8 -*-
from sklearn import svm
import pickle
import numpy
import cv2
from conta_celulas import conta_celulas
from regiao import Regiao
import pandas as pd

def svm_cells(X, y):
    svm_linear = svm.SVC()
    svm_linear.fit(X, y)

    return svm_linear

def svm_predict(svm_cells, sample):
    return svm_cells.predict(sample)


def normaliza_caracteristicas(X):
    regioes_anotadas_np = numpy.array(X)
    q_caracteristicas = regioes_anotadas_np.shape[1]

    medias = []
    desvios = []

    for i in range(q_caracteristicas):
        serie = pd.Series(regioes_anotadas_np[:,i])
        medias.append(serie.mean())
        desvios.append(serie.std())

    for r in X:
        for i in range(q_caracteristicas):
            r[i] = (r[i] - medias[i]) / desvios[i]

    return X, medias, desvios


def load_regioes_anotadas(file_name_pk, tipo):
    try:
        regioes_anotadas = pickle.load(open(file_name_pk,'rb'))
    except:
        regioes_anotadas = []
    X = []
    y = []

    for regiao in regioes_anotadas:
        X.append(regiao['caracteristicas'])
        if tipo == 0: # SVM neutrofilo vs outros
            y.append(regiao['classe'] if regiao['classe'] == 'n' else 'o' )
        else:
            y.append(regiao['classe'] if regiao['classe'] == 'l' else 'o' )
    X = numpy.array(X)
    y = numpy.array(y)
    return X, y

def classifica_imagem(svm, file_name, medias, desvios):
    imagem = cv2.imread(file_name,cv2.IMREAD_COLOR)
    regioes_encontradas = conta_celulas(imagem=imagem)

    cv2.namedWindow('imagem', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('imagem', 600,600)

    q_n = 0
    q_l = 0

    for regiao_encontrada in regioes_encontradas:
        regiao = Regiao(regiao_encontrada)
        regiao.extrai_caracteristicas()

        X = regiao.caracteristicas

        for i in range(len(medias)):
            X[i] = (X[i] - medias[i]) / desvios[i]

        classe = svm_predict(svm, [X])[0]

        if classe == 'n':
            q_n+=1
            cv2.drawContours(imagem, regiao.get_contorno(), -1, (0,255,0), 6)
        elif classe == 'l':
            q_l+=1
            cv2.drawContours(imagem, regiao.get_contorno(), -1, (255,0,0), 6)
        else:
            cv2.drawContours(imagem, regiao.get_contorno(), -1, (0,0,255), 6)

    print(q_n)
    print(q_l)
    cv2.imshow('imagem', imagem)
    k = cv2.waitKey(0)

X, y = load_regioes_anotadas('regioes_anotadas.p', 1)
X, medias, desvios = normaliza_caracteristicas(X=X)
svm = svm_cells(X, y)
classifica_imagem(svm, "/home/nayara/Desktop/TCC/index_image/41.jpg", medias, desvios)
