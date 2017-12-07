import numpy as np
from sklearn import svm

svm_neutrofilo = None
svm_linfocito = None

def treina_classificacao(vetores_caracteristicas, classes):
    global svm_neutrofilo
    svm_neutrofilo = svm.SVC(kernel="linear", probability=True)
    svm_neutrofilo.fit(vetores_caracteristicas, np.array(classes) == "n")
    
    global svm_linfocito
    svm_linfocito = svm.SVC(kernel="linear", probability=True)
    svm_linfocito.fit(vetores_caracteristicas, np.array(classes) == "l")
    
def classifica(caracteristicas):
    if svm_neutrofilo is None:
        raise Exception("SVM nao foi treinada")
    
    certeza_neut = svm_neutrofilo.predict_proba([caracteristicas])
    certeza_linfo = svm_linfocito.predict_proba([caracteristicas])
    classe = max(range(3),  key=(lambda x: ([certeza_neut[0,1], certeza_linfo[0,1], 0.5])[x]))
    return [["n", "l", "o"][classe], certeza_neut[0,1], certeza_linfo[0,1]]