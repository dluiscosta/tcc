import cv2
import numpy

caracteristicas = []

def area(regiao): #0
    return (cv2.contourArea(regiao[0]) - sum(map(cv2.contourArea, regiao[1:]))) or 0

def perimetro(regiao): #1
    return sum(map(lambda cnt: cv2.arcLength(cnt, True), regiao))

def tem_buraco(regiao): #2
    return len(regiao) > 1

def area_retangulo(regiao):
    x, y, w, h = cv2.boundingRect(regiao[0])
    return w * h

def diff_retangulo_regiao(regiao):
    return area_retangulo(regiao) - area(regiao)

def area_min_retangulo(regiao):
    p, medidas, t = cv2.minAreaRect(regiao[0])
    w, h = medidas
    return w * h

def diff_min_retangulo_regiao(regiao):
    return area_min_retangulo(regiao) - area(regiao)

def area_ciculo(regiao):
    p,radius = cv2.minEnclosingCircle(regiao[0])
    return 2 * numpy.pi * (radius**2)

def diff_circulo_regiao(regiao):
    return area_ciculo(regiao) - area(regiao)

def area_hull(regiao):
    return cv2.contourArea(cv2.convexHull(regiao[0]))

def diff_hull_regiao(regiao):
    return area_hull(regiao) - area(regiao)

caracteristicas = [area, perimetro, tem_buraco, ]

def extracao_caracteristicas(regiao, #lista de contornos, sendo o primeiro externo e os demais internos
                             idx_caracteristicas #lista com os indices das caracteristicas utilizadas
                             ):
    return map(lambda car: car(regiao),[caracteristicas[i] for i in idx_caracteristicas])
