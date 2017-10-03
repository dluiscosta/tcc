import cv2
import cv2.cv
import argparse
from exibir_imagens import show_multiple_images 
    
#Parser de parâmetros do script
parser = argparse.ArgumentParser(description="Limiarização por divergência fuzzy.")
parser.add_argument("input", help="Nome do arquivo da imagem de entrada.", action="store")
parser.add_argument("-s", "--salvar", help="Nome do arquivo da imagem de saída.", action="store")
parser.add_argument("-a", "--analise", help="Modo de análise.", action="store_true")
args = parser.parse_args()


#Imagens a serem exibidas
steps = []


#Abre a imagem de entrada e considera apenas o canal azul
input_filename = args.input
image = cv2.imread(input_filename, cv2.IMREAD_GRAYSCALE)

if args.analise:
    steps.append(cv2.cvtColor(image, cv2.cv.CV_GRAY2RGB))


#Extrai o histograma
histograma = cv2.calcHist([image], [0], None, [256], [0, 256])

if args.analise:
    from matplotlib import pyplot as plt
    plt.plot(histograma, color = 'b')
    plt.xlim([0,256])
    plt.show()
 
#----- Fuzzy Divergence -----
from math import pi as pi
from math import e as e
c = float(1)/(255 - 0) #fator de normalização
gamma = 30

#para com uma imagem idealmente segmentada
def divergencia_fuzzy(limiar, mi_b, mi_f):
    divergencia = 0
    pertinencias = []
    for intensidade in range(0, 256):
        #calcula valor de pertinencia de um pixel desta intensidade à sua
        #região associada
        if intensidade <= limiar:
            mi = mi_b
        else:
            mi = mi_f
        
        #distribuição Cauchy geral
        pertinencia = 1/((pi*gamma)*(1 + ((intensidade - mi)/gamma)**2))
        #artigo gosh
        #pertinencia = (c/pi)*(1/(1+(intensidade-mi)**2))
        
        pertinencias.append(pertinencia)
        
        #soma ao cálculo da divergência fuzzy a parcela referente a esta
        #intensidade
        divergencia += histograma[intensidade, 0]*(2
                             - pertinencia*e**(1-pertinencia)
                             - (2-pertinencia)*e**(pertinencia-1)
                             )
   
    """
    from matplotlib import pyplot as plt
    plt.plot(pertinencias, color = 'b')
    plt.xlim([0,256])
    plt.show()
    print(limiar, mi_b, mi_f, divergencia)
    """
   
    return divergencia
    
#inicia a quantidade de pixels e soma da intensidades no back e foreground
limiar_inicial = 0 #última intensidade do background
sum_intensidade_b = 0
sum_intensidade_f = 0
for intensidade in range(1, 256):
    sum_intensidade_f += intensidade*histograma[intensidade, 0]
qtd_b = histograma[0, 0]
qtd_f = histograma[:, 0].sum() - histograma[0, 0]
if qtd_b == 0: #evita divisão por 0
    mi_b = 0
else:
    mi_b = sum_intensidade_b/qtd_b
if qtd_f == 0: #evita divisão por 0
    mi_f = 0
else:
    mi_f = sum_intensidade_f/qtd_f
    
#inicia o limiar inicial como ótimo para futura comparação
menor_divergencia = divergencia_fuzzy(limiar_inicial, mi_b, mi_f)
melhor_limiar = limiar_inicial

#faz a busca linear pelo limiar que otimiza a divergência fuzzy
divergencias = [menor_divergencia]
for limiar in range(1, 255):
    #modifica a quantidade de pixels e soma da intensidades no back e foreground
    #com base na quantidade de pixels mudando de região
    qtd_mudando_regiao = histograma[limiar, 0]
    sum_intensidade_b += limiar*qtd_mudando_regiao
    sum_intensidade_f -= limiar*qtd_mudando_regiao
    qtd_b += qtd_mudando_regiao
    qtd_f -= qtd_mudando_regiao
    if qtd_b == 0: #evita divisão por 0
        mi_b = 0
    else:
        mi_b = sum_intensidade_b/qtd_b
    if qtd_f == 0: #evita divisão por 0
        mi_f = 0
    else:
        mi_f = sum_intensidade_f/qtd_f
        
    #se essa opção for melhor que a atualmente ótima, a substitue
    divergencia = divergencia_fuzzy(limiar, mi_b, mi_f)
    if divergencia < menor_divergencia:
        menor_divergencia = divergencia
        melhor_limiar = limiar

    if args.analise:
        divergencias.append(divergencia)
        
if args.analise:
    print (melhor_limiar, menor_divergencia)

#aplica o limiar ótimo encontrado na limiarização
segment = cv2.threshold(image, melhor_limiar, 255, cv2.THRESH_BINARY)
if args.analise: 
    steps.append(cv2.cvtColor(segment[1], cv2.cv.CV_GRAY2RGB))

#usa metade do limiar como instruído no artigo do Ghosh de 2010 para se 
#encontrar os núcleos
segment_div_2 = cv2.threshold(image, melhor_limiar/2, 255, cv2.THRESH_BINARY)
if args.analise: 
    steps.append(cv2.cvtColor(segment_div_2[1], cv2.cv.CV_GRAY2RGB))
    
#----- /Fuzzy Divergence -----


#Exibe os passos do procedimento
if args.analise:
    show_multiple_images(steps, "Passo a passo")
