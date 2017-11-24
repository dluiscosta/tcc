from regiao import Regiao
from conta_celulas import conta_celulas
from random import randint
import cv2
import pickle

PATH = "/home/nayara/Desktop/TCC/index_image/"

def anotar_regioes(numero_regioes, path):

    try:
        regioes_anotadas = pickle.load(open('regioes_anotadas.p','rb'))
    except:
        regioes_anotadas = []

    for i in range(0, numero_regioes):
        index_image = randint(1,129)
        file_name = path + str(index_image) + ".jpg"
        imagem = cv2.imread(file_name,cv2.IMREAD_COLOR)
        regioes = conta_celulas(imagem=imagem)
        quantidade_regioes = len(regioes)
        index_region = randint(0, quantidade_regioes-1)

        cv2.namedWindow('imagem', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('imagem', 600,600)
        cv2.drawContours(imagem, regioes[index_region][0], -1, (0,0,255), 6)
        cv2.imshow('imagem', imagem)

        regiao = Regiao(regioes[index_region])
        regiao.extrai_caracteristicas()

        # 1 : 'n'eutrofilo
        # 2 : 'l'eucocito
        # 3 : outros
        k = cv2.waitKey(0)

        if k == 1114033:
            print('NEUTROFILO')
            regiao.classe = 'n'
        elif k == 1114034:
            print('LEUCOCITO')
            regiao.classe = 'l'
        elif k == 1114035:
            print('OUTRO')
            regiao.classe = 'o'
        else:
            print("Nada")

        if regiao.classe is not None:
            regioes_anotadas.append(regiao.get_dict())

    pickle.dump(regioes_anotadas, open("regioes_anotadas.p", "wb"))


anotar_regioes(300, PATH)