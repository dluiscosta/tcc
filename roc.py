import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
import pickle
# from SVM import normaliza_caracteristicas
from base import base
from extracao_caracteristicas import extracao_caracteristicas
import cv2
import pandas as pd

def normaliza_caracteristicas(X):
    regioes_anotadas_np = np.array(X)
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

regioes_anotadas = base.get_regioes((lambda x: x.classe in ["o", "l", "n"]))
PATH_INDEX_IMAGENS = '/home/nayara/Desktop/TCC/imagens_index_manual/{}.jpg'

imagens = []

X = []
y = []
for regiao in regioes_anotadas:
    imagem_name = PATH_INDEX_IMAGENS.format(regiao.imagem)
    imagem = cv2.imread(imagem_name,cv2.IMREAD_COLOR)
    cs = extracao_caracteristicas(regiao.contornos, imagem, [i for i in range(11)], False)
    X.append(cs)
    if regiao.classe == 'l':
        classe = 0
    if regiao.classe == 'n' or regiao.classe == 'o':
        classe = 1
    # if regiao.classe == 'o':
    #     classe = 2
    y.append(classe)

X, medias, desvios = normaliza_caracteristicas(X)
y = label_binarize(y, classes=[0, 1, 2])

X = np.array(X)

n_classes = y.shape[1]

random_state = np.random.RandomState(0)
n_samples, n_features = X.shape
X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=random_state)
classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True, random_state=random_state))
y_score = classifier.fit(X_train, y_train).decision_function(X_test)


# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += interp(all_fpr, fpr[i], tpr[i])

mean_tpr /= n_classes

lw = 2
plt.figure()
colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
for i, color in zip(range(n_classes), colors):
    if(i==2):
        break
    plt.plot(fpr[i], tpr[i], color=color, lw=lw,
             label='ROC curve of class {0} (area = {1:0.2f})'
             ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=lw)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC')
plt.legend(loc="lower right")
plt.show()
