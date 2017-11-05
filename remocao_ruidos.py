import cv2

def filtro_media(imagem, size=5):
    return cv2.blur(imagem, (size, size))

def filtro_mediana(imagem, size=5):
    return cv2.medianBlur(src=imagem, ksize=size)

def filtro_gaussiano(imagem, size=5):
    return cv2.GaussianBlur(imagem, (size, size), sigmaX=0)

def remocao_ruidos(imagem, analise=False):
    #Aplica o filtro de mediana com kernel de tamanho 9x9.
    return filtro_mediana(imagem, 9)