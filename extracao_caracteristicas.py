import cv2
import numpy as np

#Caracteristicas geometricas

def area(regiao): #0
    return (cv2.contourArea(regiao[0]) - sum(map(cv2.contourArea, regiao[1:])))

def area_convex_hull(regiao): #1
    return cv2.contourArea(cv2.convexHull(regiao[0]))

def solidez(regiao): #2
    ach = area_convex_hull(regiao)
    return area(regiao)/ach if ach != 0 else 0

def perimetro(regiao): #3
    return sum(map(lambda cnt: cv2.arcLength(cnt, True), regiao))

def compactividade(regiao): #4
    p2 = perimetro(regiao)**2
    return area(regiao)/p2 if p2 != 0 else 0

def circularidade(regiao): #5
    _, raio = cv2.minEnclosingCircle(regiao[0])
    a = area(regiao)
    return (np.pi * raio**2)/a if a != 0 else 0

def retangularidade(regiao): #6
    _, medidas, _ = cv2.minAreaRect(regiao[0])
    w, h = medidas
    a = area(regiao)
    return float(w*h)/a if a != 0 else 0

def tem_buraco(regiao): #7
    return len(regiao) > 1

caracteristicas_geometricas = [area, area_convex_hull, solidez, perimetro, compactividade, circularidade, retangularidade, tem_buraco]


#Caracteristicas de textura

def media(pixels): #8
    return np.mean(pixels)

def variancia(pixels): #9
    return np.var(pixels)

def desvio_padrao(pixels): #10
    return np.std(pixels)

caracteristicas_textura = [media, variancia, desvio_padrao]

medias, desvios_padroes = np.zeros((2, len(caracteristicas_geometricas) + len(caracteristicas_textura)), dtype=float)
normalizado = False

#Calcula a media e o desvio padrao das imagens em um conjunto de treinamento
#para posterior normalizacao das caracteristicas
def define_normalizacao(regioes, imagens):
    caracteristicas = map(lambda x: np.array(extracao_caracteristicas(*x, idx_caracteristicas = range(11), normalizar=False)),
                          zip(regioes, imagens))
    
    global medias
    medias = np.mean(caracteristicas, axis=0)
    
    global desvios_padroes
    desvios_padroes = np.std(caracteristicas, axis=0)
    
    global normalizado
    normalizado = True

def checa_normalizacao():
    return (medias, desvios_padroes)

def extracao_caracteristicas(regiao, #lista de contornos, sendo o primeiro externo e os demais internos
                             imagem,
                             idx_caracteristicas, #lista com os indices das caracteristicas utilizadas
                             normalizar=True):
    
    c_g = map(lambda car: car(regiao),[caracteristicas_geometricas[i] 
              for i in idx_caracteristicas if i < len(caracteristicas_geometricas)])
    
    #Encontra os pixels internos a regiao
    im_c = cv2.cvtColor(imagem, cv2.cv.CV_BGR2GRAY)
    mascara = np.zeros(im_c.shape, dtype=np.uint8)
    cv2.drawContours(mascara, [regiao[0]], -1, 255, -1)
    cv2.drawContours(mascara, regiao[1:], -1, 0, -1)
    pixels_internos = im_c[mascara == 255]

    c_t = map(lambda car: car(pixels_internos),[caracteristicas_textura[i-len(caracteristicas_geometricas)] 
              for i in idx_caracteristicas if i >= len(caracteristicas_geometricas)])
    
    cs = np.array(c_g + c_t)
    
    if normalizar:
        if normalizado:
            cs = (cs - medias)/desvios_padroes
        else:
            raise("Normalizacao nao foi definida!")
        
    return cs
