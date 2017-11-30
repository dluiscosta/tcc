from regiao import Regiao
from conta_celulas import conta_celulas
from random import randint
import cv2
import pickle
import numpy as np

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
        # cv2.drawContours(imagem, regioes[index_region][0], -1, (0,0,255), 3)

        # rect = cv2.minAreaRect(regioes[index_region][0])
        # box = cv2.cv.BoxPoints(rect)
        # box = np.int0(box)
        # cv2.drawContours(imagem,[box],0,(0,0,255),6)
        #
        # x,y,w,h = cv2.boundingRect(regioes[index_region][0])
        # cv2.rectangle(imagem,(x,y),(x+w,y+h),(0,255,0),6)

        # (x,y),radius = cv2.minEnclosingCircle(regioes[index_region][0])
        # center = (int(x),int(y))
        # radius = int(radius)
        # cv2.circle(imagem,center,radius,(0,0,255),5)

        hull = cv2.convexHull(regioes[index_region][0])
        cv2.drawContours(imagem,[hull],0,(0,0,255),5)

        cv2.imshow('imagem', imagem)

        regiao = Regiao(regioes[index_region])
        regiao.extrai_caracteristicas()

        # 1 : 'n'eutrofilo
        # 2 : 'l'infocito
        # 3 : outros
        k = cv2.waitKey(0)

        if k == 1114033:
            print('NEUTROFILO')
            regiao.classe = 'n'
        elif k == 1114034:
            print('LINFOCITO')
            regiao.classe = 'l'
        elif k == 1114035:
            print('OUTRO')
            regiao.classe = 'o'
        else:
            print("Nada")

        if regiao.classe is not None:
            regioes_anotadas.append(regiao.get_dict())

    pickle.dump(regioes_anotadas, open("regioes_anotadas.p", "wb"))


# anotar_regioes(600, PATH)

regioes_anotadas = pickle.load(open('regioes_anotadas.p','rb'))

area_n = 0
area_l = 0
area_o = 0
perimetro_n = 0
perimetro_l = 0
perimetro_o = 0
area_retangulo_n = 0
area_retangulo_l = 0
area_retangulo_o = 0
diff_retangulo_regiao_n = 0
diff_retangulo_regiao_l = 0
diff_retangulo_regiao_o = 0
area_min_retangulo_n = 0
area_min_retangulo_l = 0
area_min_retangulo_o = 0
diff_min_retangulo_regiao_n = 0
diff_min_retangulo_regiao_l = 0
diff_min_retangulo_regiao_o = 0
area_ciculo_n = 0
area_ciculo_l = 0
area_ciculo_o = 0
diff_circulo_regiao_n = 0
diff_circulo_regiao_l = 0
diff_circulo_regiao_o = 0
area_hull_n = 0
area_hull_l = 0
area_hull_o = 0
diff_hull_regiao_n = 0
diff_hull_regiao_l = 0
diff_hull_regiao_o = 0
q_tem_buraco_n = 0
q_tem_buraco_l = 0
q_tem_buraco_o = 0
q_n = 0
q_l = 0
q_o = 0

for r in regioes_anotadas:
    if r['classe'] == 'n':
        q_n += 1
        area_n += r['caracteristicas'][0]
        perimetro_n += r['caracteristicas'][1]
        area_retangulo_n += r['caracteristicas'][3]
        diff_retangulo_regiao_n += r['caracteristicas'][4]
        area_min_retangulo_n += r['caracteristicas'][5]
        diff_min_retangulo_regiao_n += r['caracteristicas'][6]
        area_ciculo_n += r['caracteristicas'][7]
        diff_circulo_regiao_n += r['caracteristicas'][8]
        area_hull_n += r['caracteristicas'][9]
        diff_hull_regiao_n += r['caracteristicas'][10]
        if r['caracteristicas'][2] == 1:
            q_tem_buraco_n += 1

    if r['classe'] == 'l':
        q_l += 1
        area_l += r['caracteristicas'][0]
        perimetro_l += r['caracteristicas'][1]
        area_retangulo_l += r['caracteristicas'][3]
        diff_retangulo_regiao_l += r['caracteristicas'][4]
        area_min_retangulo_l += r['caracteristicas'][5]
        diff_min_retangulo_regiao_l += r['caracteristicas'][6]
        area_ciculo_l += r['caracteristicas'][7]
        diff_circulo_regiao_l += r['caracteristicas'][8]
        area_hull_l += r['caracteristicas'][9]
        diff_hull_regiao_l += r['caracteristicas'][10]
        if r['caracteristicas'][2] == 1:
            q_tem_buraco_l += 1

    if r['classe'] == 'o':
        q_o += 1
        area_o += r['caracteristicas'][0]
        perimetro_o += r['caracteristicas'][1]
        area_retangulo_o += r['caracteristicas'][3]
        diff_retangulo_regiao_o += r['caracteristicas'][4]
        area_min_retangulo_o += r['caracteristicas'][5]
        diff_min_retangulo_regiao_o += r['caracteristicas'][6]
        area_ciculo_o += r['caracteristicas'][7]
        diff_circulo_regiao_o += r['caracteristicas'][8]
        area_hull_o += r['caracteristicas'][9]
        diff_hull_regiao_o += r['caracteristicas'][10]
        if r['caracteristicas'][2] == 1:
            q_tem_buraco_o += 1

print('area_n: {}'.format(area_n/q_n))
print('area_l: {}'.format(area_l/q_l))
print('area_o: {}'.format(area_o/q_o))
print('perimetro_n: {}'.format(perimetro_n/q_n))
print('perimetro_l: {}'.format(perimetro_l/q_l))
print('perimetro_o: {}'.format(perimetro_o/q_o))
print('area_retangulo_n: {}'.format(area_retangulo_n/q_n))
print('area_retangulo_l: {}'.format(area_retangulo_l/q_l))
print('area_retangulo_o: {}'.format(area_retangulo_o/q_o))
print('diff_retangulo_regiao_n: {}'.format(diff_retangulo_regiao_n/q_n))
print('diff_retangulo_regiao_l: {}'.format(diff_retangulo_regiao_l/q_l))
print('diff_retangulo_regiao_o: {}'.format(diff_retangulo_regiao_o/q_o))
print('area_min_retangulo_n: {}'.format(area_min_retangulo_n/q_n))
print('area_min_retangulo_l: {}'.format(area_min_retangulo_l/q_l))
print('area_min_retangulo_o: {}'.format(area_min_retangulo_o/q_o))
print('diff_min_retangulo_regiao_n: {}'.format(diff_min_retangulo_regiao_n/q_n))
print('diff_min_retangulo_regiao_l: {}'.format(diff_min_retangulo_regiao_l/q_l))
print('diff_min_retangulo_regiao_o: {}'.format(diff_min_retangulo_regiao_o/q_o))
print('area_ciculo_n: {}'.format(area_ciculo_n/q_n))
print('area_ciculo_l: {}'.format(area_ciculo_l/q_l))
print('area_ciculo_o: {}'.format(area_ciculo_o/q_o))
print('diff_circulo_regiao_n: {}'.format(diff_circulo_regiao_n/q_n))
print('diff_circulo_regiao_l: {}'.format(diff_circulo_regiao_l/q_l))
print('diff_circulo_regiao_o: {}'.format(diff_circulo_regiao_o/q_o))
print('area_hull_n: {}'.format(area_hull_n/q_n))
print('area_hull_l: {}'.format(area_hull_l/q_l))
print('area_hull_o: {}'.format(area_hull_o/q_o))
print('diff_hull_regiao_n: {}'.format(diff_hull_regiao_n/q_n))
print('diff_hull_regiao_l: {}'.format(diff_hull_regiao_l/q_l))
print('diff_hull_regiao_o: {}'.format(diff_hull_regiao_o/q_o))
print('q_tem_buraco_n: {}'.format(q_tem_buraco_n))
print('q_tem_buraco_l: {}'.format(q_tem_buraco_l))
print('q_tem_buraco_o: {}'.format(q_tem_buraco_o))

print('NEUTROFILOS:{}'.format(q_n))
print('LINFOCITOS:{}'.format(q_l))
print('OUTROS:{}'.format(q_o))
