from modulos import *

def conta_celulas(imagem, analise=False):
    im_l = do(imagem, analise=analise) #delimita a lamina
    im_f = rr(imagem, analise=analise) #remove ruidos
    im_b = limiarizacao(im_f, im_l, analise=analise) #limiariza o interior da lamina
    regioes = er(im_b, analise=analise, original=imagem) #extrai regioes
    return regioes
