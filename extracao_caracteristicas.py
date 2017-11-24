import cv2
import numpy

caracteristicas = []

# ler artigo SARASWAT

def area(regiao): #0
    return (cv2.contourArea(regiao[0]) - sum(map(cv2.contourArea, regiao[1:]))) or 0

def perimetro(regiao): #1
    return sum(map(lambda cnt: cv2.arcLength(cnt, True), regiao))

def tem_buraco(regiao): #2
    return 1 if len(regiao) > 1 else 0

def area_retangulo(regiao): #3
    x, y, w, h = cv2.boundingRect(regiao[0])
    return w * h

def diff_retangulo_regiao(regiao): #4
    return area_retangulo(regiao) - area(regiao)

def area_min_retangulo(regiao): #5
    p, medidas, t = cv2.minAreaRect(regiao[0])
    w, h = medidas
    return w * h

def diff_min_retangulo_regiao(regiao): #6
    return area_min_retangulo(regiao) - area(regiao)

def area_ciculo(regiao): #7
    p,radius = cv2.minEnclosingCircle(regiao[0])
    return 2 * numpy.pi * (radius**2)

def diff_circulo_regiao(regiao): #8
    return area_ciculo(regiao) - area(regiao)

def area_hull(regiao): #9
    return cv2.contourArea(cv2.convexHull(regiao[0]))

def diff_hull_regiao(regiao): #10
    return area_hull(regiao) - area(regiao)

caracteristicas = [area, perimetro, tem_buraco, area_retangulo, diff_retangulo_regiao, area_min_retangulo, diff_min_retangulo_regiao, area_ciculo, diff_circulo_regiao, area_hull, diff_hull_regiao]

def extracao_caracteristicas(regiao, #lista de contornos, sendo o primeiro externo e os demais internos
                             idx_caracteristicas #lista com os indices das caracteristicas utilizadas
                             ):
    return map(lambda car: car(regiao),[caracteristicas[i] for i in idx_caracteristicas])
