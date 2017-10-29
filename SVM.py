# -*- coding: utf-8 -*-
from sklearn import svm

# usando arrays fakes -- precisa colocar as caracteristicas em array
# X = np.array([[6.7,3.0,5.2,2.3], [6.3,2.5,5.0,1.9], [6.5,3.0,5.2,2.0], [6.2,3.4,5.4,2.3], [5.9,3.0,5.1,1.8]])
# y = np.array([1, 1, 1, 2, 2]) -> classe a qual cada uma das amostras de X pertence

def svm_cells(X, y):
    svm_linear = svm.SVC
    svm_linear.fit(X, y)

    return svm_linear

def svm_predict(svm_cells, sample):
    return svm_cells.predict(sample)

# no caso do nosso, teremos que usar 2 SVMs onde a primeira classifica entre neutrófilo e não neutrófilo e a segunda entre monócito e não monócito, certo
