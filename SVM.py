# -*- coding: utf-8 -*-
from sklearn import svm
import pickle
import numpy


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
    print(regioes_anotadas)
    X = []
    y = []
    for regiao in regioes_anotadas:
        X.append(regiao['caracteristicas'])
        y.append(regiao['classe'])
    X = numpy.array(X)
    y = numpy.array(y)
    return X, y

# X, y = load_regioes_anotadas('lalala')
# svm = svm_cells(X, y)

# print(svm_predict(svm, sample))
