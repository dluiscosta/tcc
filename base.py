import cv2
import cv2.cv
import numpy as np
from exibir_imagens import mostra_imagens

#Ordem em que a base sera anotada.
la1 = [111, 128, 77, 82, 86, 115, 90, 81, 13, 8, 47, 5, 93, 36, 26, 53, 54, 79,
       18, 73, 40, 125, 87, 11, 14, 15, 123, 37, 74, 99, 59, 42, 67, 23, 38,
       116, 12, 100, 122, 95, 17, 6, 45, 94, 127, 39, 27, 109, 19, 65, 52, 105,
       10, 120, 9, 21, 31, 44, 22, 85, 3, 49, 28, 68, 50, 25, 43, 46, 35, 71, 80,
       51, 34, 20, 126, 56, 1, 30, 7, 96, 33, 76, 4, 57, 24, 106, 64, 55, 32, 16,
       108, 63, 101, 118, 60, 107, 124, 48, 113, 70, 110, 114, 61, 97, 104, 83,
       117, 112, 98, 92, 91, 62, 75, 102, 66, 121, 58, 29, 88, 119, 89, 72, 103,
       84, 41, 0, 2, 69, 78]

shape_imagens = (4160, 3120) #altura, largura
shape_patch = (500, 500) #altura, largura

class Celula:
    def __init__(self, indice, tipo, componentes, buracos):
        self.indice = indice 
        self.tipo = tipo # 'n'eutrofilo, 'l'eucocito, 'm'onocito
        self.componentes = componentes
        self.buracos = buracos
        self.area = None
        
    def get_area(self):
        if hasattr(self, 'area') and self.area is not None:
            return self.area
        else:
            im = np.zeros(shape_patch, dtype="uint8")
            
            #Desenha a celula na primeira imagem
            cv2.drawContours(im, self.componentes, -1, [255], -1)
            cv2.drawContours(im, self.componentes, -1, [255], 2)
            cv2.drawContours(im, self.buracos, -1, [0], -1)
            
            #Conta os pixels do foreground
            self.area = np.count_nonzero(im)
            return self.area            
            
        
class Lamina:
    #Recebe opcionalmente como parametros as coordenadas do canto superior 
    #esquerdo e o formato (largura e altura) do retangulo no qual a elipse
    #encaixada no GIMP esta inscrita.
    def __init__(self, canto = None, shape = None):
        if canto is None:
            self.raio = None
            self.centro = None
        else:
            self.raio = (shape[0] + shape[1])/4
            self.centro = (canto[0] + self.raio, canto[1] + self.raio) 

    #Retorna uma imagem binaria que serve como mascara para a regiao da lamina.
    def get_imagem(self):
        imagem = np.zeros(shape_imagens, dtype=np.uint8)
        cv2.circle(imagem, self.centro, self.raio, 255, thickness=-1)
        return imagem

    #Checa se um ponto esta dentro da lamina.
    def esta_dentro(self, p):
        return ((self.centro[0] - p[0])**2 + (self.centro[1] - p[1])**2
                < self.raio**2)

    #Checa se a regiao de um patch esta completamente dentro da lamina atraves
    #da checagem dos quatro cantos.
    def patch_esta_dentro(self, patch):
        h, w = shape_patch
        x, y = patch.canto
        return (self.esta_dentro((x, y)) and self.esta_dentro((x + w, y)) and 
                self.esta_dentro((x + w, y + h)) and self.esta_dentro((x, y + h)))
            
    def avaliar_lamina(self, tentativa, analise=False, indice=None):
        im = self.get_imagem()
        
        import numpy as np
        comp = np.zeros(shape_imagens + (3,), dtype=np.uint8)
        comp[:,:,0] = im
        comp[:,:,2] = tentativa
             
        hist = cv2.calcHist([comp], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
        perdidos = hist[255,0,0] #pixels da lamina anotada que nao foram pegos
        excesso = hist[0,0,255] #pixels que foram pegos a mais
        #Atribui mais peso a area exterior a lamina que foi pega e pode,
        #nos proximos passos, gerar regioes nao legitimas na periferia da lamina.
        nota = perdidos + 3*excesso 
        nota = nota/(shape_imagens[0]*shape_imagens[1]) #normaliza
        nota = 1-nota #quanto maior melhor
                     
        if analise:
            if indice is None:
                mostra_imagens([comp], "")
            else:
                original = cv2.imread("base\\" + str(indice) + ".jpg", cv2.IMREAD_COLOR)
                rosa = np.array([255, 0, 255], dtype="uint8")
                comum = cv2.inRange(comp, rosa, rosa)
                contours, hierarchy = cv2.findContours(comum, 
                                               cv2.RETR_CCOMP,
                                               cv2.CHAIN_APPROX_NONE)
                cv2.drawContours(original, contours, -1, (0,255,0), 3)
                mostra_imagens([comp, original], "")
            print "Pixels perdidos: " + str(perdidos)
            print "Pixels pegos em excesso: " + str(excesso)
            print "\n\n"

        return nota
         
def distancia_jaccard(im1, im2):
    #Calcula a distancia de Jaccard
    interseccao = np.count_nonzero(cv2.bitwise_and(im1, im2))
    uniao = np.count_nonzero(cv2.bitwise_or(im1, im2))    
    jaccard_index = float(interseccao)/float(uniao) if uniao != 0 else 1

    return 1 - jaccard_index
    
class Patch:
    def __init__(self, canto = (None, None), indice = None):
        self.canto = canto #(x, y) canto superior esquerdo
        self.indice = indice
        self.celulas = None
        
    def get_imagem(self):
        x, y = self.canto
        h, w = shape_patch
        imagem = cv2.imread("base\\" + str(self.indice) + ".jpg", cv2.IMREAD_COLOR)
        return imagem[y : y + h, x : x + w]
        
    def anota_celulas(self, imagem_anotacoes):
        cels = []
        ind = 0
        for tipo in [(0, 'l'), (160, 'm'), (255, 'n')]: #para cada tipo de celula              
            for r in range(0, 50):
                #Extrai os contornos das regioes com um valor de R
                val = np.array([int(tipo[0]), 0, r])
                im = cv2.inRange(imagem_anotacoes, val, val)
                contours, hierarchy = cv2.findContours(im, 
                       cv2.RETR_CCOMP, #associa contornos de componentes com contornos de buracos
                       cv2.CHAIN_APPROX_NONE) #armazena todos os pontos no contorno
                
                #Itera pelos contornos e constroi as celulas
                if r == 0: #cada regiao conexa eh uma celula diferente
                    for i in range(0, len(contours)):
                        if hierarchy[0,i,3] == -1: #nao tem pai -> eh contorno exterior
                            comp = [contours[i]]
                            bur = []
                            if hierarchy[0,i,2] != -1: #ha filho(s) -> ha buraco(s)
                                i2 = hierarchy[0,i,2] #primeiro filho
                                bur.append(contours[i2])
                                while hierarchy[0,i2,0] != -1: #itera pelos outros filhos
                                    i2 = hierarchy[0,i2,0]
                                    bur.append(contours[i2])
                            cels.append(Celula(self.indice*1000 + ind, tipo[1], comp, bur))
                            ind = ind + 1
                else: #todas regioes nesse valor de R sao uma unica celula
                    comp = []
                    bur = []
                    for i in range(0, len(contours)):
                        if hierarchy[0,i,3] == -1: #nao tem pai -> eh contorno exterior
                            comp.append(contours[i])
                        else: #tem pai -> eh contorno interior (buraco)
                            bur.append(contours[i])
                    if comp:
                        cels.append(Celula(self.indice*1000 + ind, tipo[1], comp, bur))
                        ind = ind + 1
        self.celulas = cels
        
    #Calcula a distancia de Jaccard de uma predicao (imagem binaria) para com o padrao-ouro
    def avaliacao_distancia_jaccard(self, predicao):
        #Gera a imagem do padrao-ouro com base nos contornos anotados das celulas
        ouro = np.zeros(shape_patch, dtype=np.uint8)
        for celula in self.celulas:
            cv2.drawContours(ouro, celula.componentes, -1, [255], -1) #preenchimento
            cv2.drawContours(ouro, celula.componentes, -1, [255], 2) #borda
            cv2.drawContours(ouro, celula.buracos, -1, [0], -1) #buracos

        return distancia_jaccard(ouro, predicao)
            
    #Para cada celula anotada, escolhe por forca bruta a regiao da predicao que mais se aproxima dela.
    #Retorna o somatorio das diferencas entre cada celula e a sua regiao correspondente.
    def avaliacao_forca_bruta(self, predicao, diferenca, analise = False):
        if self.celulas is None:
            raise Exception("As celulas nao foram anotadas!")
        
        contornos, hierarquia = predicao
        
        #Separa as regioes da predicao
        idxs = range(len(contornos))
        regioes = [(contornos[i], [contornos[j] for j in idxs if hierarquia[0,j,3] == i]) #seleciona ele e seus filhos
                   for i in idxs if hierarquia[0,i,3] == -1] #para cada pai
            
        #Compara uma celula com uma regiao
        im1, im2 = np.zeros((2,) + shape_patch, dtype=np.uint8) #gera duas imagens pretas para comparacao
        def compara(celula, regiao):
            #Desenha a celula na primeira imagem
            cv2.drawContours(im1, cel.componentes, -1, [255], -1) #preenchimento
            cv2.drawContours(im1, cel.componentes, -1, [255], 2) #borda
            cv2.drawContours(im1, cel.buracos, -1, [0], -1) #buracos
        
            #Desenha a regiao na segunda imagem
            componente, buracos = regiao
            cv2.drawContours(im2, [componente], -1, [255], -1) #preenchimento
            cv2.drawContours(im2, [componente], -1, [255], 2) #borda
            cv2.drawContours(im2, buracos, -1, [0], -1) #buracos
            
            #Calcula a diferenca com a funcao fornecida
            dif = diferenca(im1, im2)
            
            #Restaura as imagens pretas
            cv2.drawContours(im1, cel.componentes, -1, [0], -1) #preenchimento
            cv2.drawContours(im1, cel.componentes, -1, [0], 2) #borda
            cv2.drawContours(im2, [componente], -1, [0], -1) #preenchimento
            cv2.drawContours(im2, [componente], -1, [0], 2) #borda

            return dif
        
        #Compara as celulas com cada regiao e guarda a menor diferenca
        min_diffs = map(lambda cel: 
                            min(map(lambda reg: compara(cel, reg), regioes)
                            + [1]), #caso nao haja regioes na predicao
                        self.celulas)
    
        if analise:
            #Inicia uma imagem branca
            im_an = np.zeros(shape_patch + (3,), dtype=np.uint8)
            im_an[:,:,:] = 255 
            
            #Desenha as regioes segmentadas em cinza
            cv2.drawContours(im_an, contornos, -1, [200, 200, 200], -1)
            cv2.drawContours(im_an, contornos, -1, [200, 200, 200], 2)
            
            #Prepara uma imagem que sera sobreposta com transparencia
            im_alpha = np.zeros(shape_patch + (3,), dtype=np.uint8)
            
            #Desenha as celulas
            import matplotlib.cm as cm
            for i,cel in enumerate(self.celulas): #para cada celula
            
                #Mapeia a menor diferenca para cores
                cor_rgba = cm.winter(1 - min_diffs[i], 1, True)
                cor_bgr = map(lambda c: int(c), list(cor_rgba[2::-1]))
                
                #Desenha o contorno da celula                
                cv2.drawContours(im_an, cel.componentes, -1, cor_bgr, 1)
                cv2.drawContours(im_an, cel.buracos, -1, cor_bgr, 1)
                
                #Desenha o preenchimento da celula, que sera transparente                
                cv2.drawContours(im_alpha, cel.componentes, -1, cor_bgr, -1)
                cv2.drawContours(im_alpha, cel.buracos, -1, [0, 0, 0], -1)

            #Ajusta a imagem a ser sobreposta com transparencia de maneira a nao afetar o restante da imagem (areas cem celulas)
            im_alpha_g = cv2.cvtColor(im_alpha, cv2.cv.CV_BGR2GRAY) #tons de cinza
            t, mask = cv2.threshold(im_alpha_g, 0, 255, cv2.THRESH_BINARY_INV) #apenas a regiao que nao tem celulas
            mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)
            im_alpha = im_alpha + im_an*mask*255  #copia da imagem com as regioes a area que nao tem celulas
            
            #Sobrepoe as imagens
            im_an = cv2.addWeighted(im_an, 0.7, im_alpha, 0.3, 0) #adiciona com transparencia            
        
            mostra_imagens([im_an], "Similaridade de regiao encontrada para cada celula")
                   
        #Retorna a media de menores diferencas entre todas as celulas
        return np.mean(min_diffs) if len(min_diffs) > 0 else 1
                        
class Imagem:
    def __init__(self, indice):
        self.indice = indice
        self.lamina = None
        self.patch = None
        self.foco = None
        self.obstruida = None
        
    def get_patch(self):
        if self.lamina is None:
            raise Exception("Voce nao definiu a lamina!")
        elif self.patch is None:
            import random as rd
            rd.seed(self.indice)
            h, w = shape_imagens
            patch = Patch(canto = (rd.randint(0, h), rd.randint(0, w)))
            while not self.lamina.patch_esta_dentro(patch):
                patch.canto = (rd.randint(0, h), rd.randint(0, w))
            patch.indice = self.indice
            self.patch = patch
            return patch
        else:
            return self.patch      
            
    def get_imagem(self):
        return cv2.imread("base\\" + str(self.indice) + ".jpg", cv2.IMREAD_COLOR)
    

class Base:
    def __init__(self):
        self.imagens = [Imagem(indice = i) for i in range(1, 130)]

    def anotar_lamina(self):
        for i in la1:
            if self.imagens[i-1].lamina is None:
                print "A proxima lamina a ser anotada eh a " + str(i)
                x = int(raw_input("Canto x: "))
                y = int(raw_input("Canto y: "))
                w = int(raw_input("Largura: "))
                h = int(raw_input("Altura: "))

                self.imagens[i-1].lamina = Lamina(canto = [x,y], shape = [w, h])
                return
        print "Todas as laminas foram anotadas"
        return
    
    def get_imagens(self, condicoes):
        return [x for x in self.imagens if condicoes(x)] 
        
    def salvar(self):
        import pickle
        with open("anotacoes.pkl", "wb") as f:
            pickle.dump(self, f)
            f.close()
      

import pickle
with open("anotacoes.pkl", "rb") as f:
    base = pickle.load(f)
    f.close()