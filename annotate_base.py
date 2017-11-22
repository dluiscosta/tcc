from regiao import Regiao
from conta_celulas import conta_celulas
from random import randint
import cv2

def anotar_regioes(numero_regioes):

    for i in range(0, numero_regioes):
        index_image = randint(1,129)
        imagem = cv2.imread('/home/nayara/Desktop/TCC/imagens2606/IMG_20170626_191737083_HDR.jpg',cv2.IMREAD_COLOR)
        regioes = conta_celulas(imagem=imagem)
        quantidade_regioes = len(regioes)
        index_region = randint(0, quantidade_regioes-1)

        cv2.namedWindow('imagem', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('imagem', 600,600)
        cv2.drawContours(imagem, regioes[index_region][0], -1, (0,255,0), 6)
        cv2.imshow('imagem', imagem)

        # 1 : 'n'eutrofilo
        # 2 : 'l'eucocito
        # 3 : outros
        k = cv2.waitKey(0)

        if k == 1114033:
            print('NEUTROFILO')
        elif k == 1114034:
            print('LEUCOCITO')
        elif k == 1114035:
            print('OUTRO')
        else:
            print("Nada")
