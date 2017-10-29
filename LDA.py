# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import numpy as np
from matplotlib import pyplot as plt


# usando arrays fakes -- precisa colocar as caracteristicas em array
# X = np.array([[6.7,3.0,5.2,2.3], [6.3,2.5,5.0,1.9], [6.5,3.0,5.2,2.0], [6.2,3.4,5.4,2.3], [5.9,3.0,5.1,1.8]])
# y = np.array([1, 1, 1, 2, 2])

def lda_cells(X, y):
    lda = LDA(n_components=2)
    X_r2 = lda.fit(X, y).transform(X)
