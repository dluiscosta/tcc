import cv2
import conta_celulas as cc

class Regiao:
    def __init__(self, regiao):
        self.regiao = regiao
        self.classe = None
        self.caracteristicas = []

    def get_contorno(self):
        return self.regiao[0]

    def extrai_caracteristicas(self):
        pass

    def draw_contorno(self, imagem):
        cv2.drawContours(imagem,self.regiao[0],-1,(0,255,0),3)
