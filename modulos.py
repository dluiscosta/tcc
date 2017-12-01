import cv2
from exibir_imagens import mostra_imagens
import numpy as np
from limiarizacao_divergencia_fuzzy import limiarizacao_divergencia_fuzzy as ldf
from extrair_regioes import extrair_regioes as er
from delimitacao_otsu import delimitacao_otsu as do
from remocao_ruidos import remocao_ruidos as rr
import base
from limiarizacao import limiarizacao
from extracao_caracteristicas import *
