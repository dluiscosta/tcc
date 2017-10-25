import cv2

caracteristicas = []

def area(regiao): #0
    return cv2.contourArea(regiao[0]) - sum(map(cv2.contourArea, regiao[1:]))

def perimetro(regiao): #1
    return sum(map(lambda cnt: cv2.arcLength(cnt, True), regiao))

def tem_buraco(regiao): #2
    return len(regiao) > 1

caracteristicas = [area, perimetro, tem_buraco]

def extracao_caracteristicas(regiao, #lista de contornos, sendo o primeiro externo e os demais internos
                             idx_caracteristicas #lista com os indices das caracteristicas utilizadas
                             ):    
    return map(lambda car: car(regiao),[caracteristicas[i] for i in idx_caracteristicas])
        
