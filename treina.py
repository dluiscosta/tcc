import extracao_caracteristicas
import classificacao
import base
from scipy import interp
import numpy as np
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt

def treina(regioes):   
    imagens = map(lambda x: x.get_imagem(), base.base.get_imagens())
    caracteristicas = extracao_caracteristicas.define_normalizacao(
            map(lambda x: x.contornos, regioes),
            map(lambda x: imagens[x.imagem-1], regioes))
    
    classificacao.treina_classificacao(caracteristicas,
                                       map(lambda x:x.classe, regioes))
    
def plota_roc():
    regioes = np.array(base.base.get_regioes(lambda x: x.classe in ["o", "l", "n"]))
    cv = StratifiedKFold(n_splits=4)
    classes = np.array(map(lambda x: x.classe, regioes))
    
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
        
    i = 0
    for train, test in cv.split(regioes, classes):
        treina(regioes[train])
        ec = extracao_caracteristicas.extracao_caracteristicas
        vectores_caracteristicas = [ec(regiao.contornos,
                                       base.base.get_imagens()[regiao.imagem-1].get_imagem(),
                                       range(11))
                                    for regiao in regioes[test]]
        pred = np.array([classificacao.classifica(carac) for carac in vectores_caracteristicas])
        
        #neutrofilo
    
        fpr, tpr, thresholds = roc_curve(np.array(map(lambda x: int(x), classes[test] == "l")),
                                         np.array(map(lambda x: float(x), pred[:, 2])))
        tprs.append(interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        plt.plot(fpr, tpr, lw=1, alpha=0.3,
                 label='ROC da dobra %d (AUC = %0.2f)' % (i, roc_auc))
        i += 1
        
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
             label='Aleatorio', alpha=.8)
    
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    plt.plot(mean_fpr, mean_tpr, color='b',
             label=r'ROC medio (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
             lw=2, alpha=.8)
    
    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                     label=r'$\pm$ 1 desv. pad.')
    
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Razao Falso Positivo')
    plt.ylabel('Razao Verdadeiro Positivo')
    plt.title('Reconhecimento de Linfocitos')
    plt.legend(loc="lower right")
    plt.show()