import cv2
import conta_celulas as cc
from extracao_caracteristicas import extracao_caracteristicas

class Regiao:
    def __init__(self, regiao):
        self.regiao = regiao
        self.classe = None
        self.caracteristicas = []

    def get_contorno(self):
        return self.regiao[0]

    def extrai_caracteristicas(self):
        self.caracteristicas = extracao_caracteristicas(self.regiao, [i for i in range(0,11)])

    def draw_contorno(self, imagem):
        cv2.drawContours(imagem,self.regiao[0],-1,(0,255,0),3)

    def get_dict(self):
        return {"classe": self.classe, "caracteristicas": self.caracteristicas}
