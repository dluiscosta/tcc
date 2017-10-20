import cv2
import cv2.cv
from exibir_imagens import mostra_imagens

def limiarizacao_divergencia_fuzzy(imagem, mascara=None, c=float(1)/(255 - 0),
                                   gamma=1, analise=False):
    if analise:
        from matplotlib import pyplot as plt
        print "- Limiarizacao por divergencia fuzzy -"
    
    if analise:
        titulo = "Imagem de entrada, apenas um canal"
        if mascara is not None:
            cortada = cv2.bitwise_and(imagem, imagem, mask=mascara)
            mostra_imagens([imagem, cortada], titulo, 
                           ["sem aplicacao da mascara", "apos aplicacao da mascara"])
        else:
            mostra_imagens(imagem, titulo)
            
    #Extrai o histograma.
    histograma = cv2.calcHist([imagem], [0], mascara, [256], [0, 256])
    if analise:
        plt.figure()
        plt.title("Histograma da imagem")
        plt.plot(range(0, 256), histograma, color = 'b')
        plt.show()
  
    #----- Fuzzy Divergence -----
    from math import pi as pi
    from math import e as e
    #Divergencia fuzzy para com uma imagem idealmente segmentada se a imagem
    #for binarizada por um determinado limiar
    def divergencia_fuzzy(limiar, mi_b, mi_f, analise=False):
        divergencia = 0
        pertinencias_b, pertinencias_f = ([], [])
        for intensidade in range(0, 256):
            #calcula valor de pertinencia de um pixel desta intensidade a sua
            #regiao associada
            if intensidade <= limiar:
                mi = mi_b
            else:
                mi = mi_f
                        
            #Com os valores de parametro padroes, a formula fica igual a em
            #Ghosh, 2010. 
            #a distribuicao Cauchy generica nao possui o parametro "c".
            pertinencia = (1/(c*pi*gamma))*(
                    1/(1 + ((intensidade - mi)/gamma)**2))    
        
            if analise:
                if intensidade <= limiar:
                    pertinencias_b.append(pertinencia)
                else:
                    pertinencias_f.append(pertinencia)
                
            #Soma ao calculo da divergencia fuzzy a parcela referente a esta
            #intensidade.
            divergencia += histograma[intensidade, 0]*(2
                                 - pertinencia*e**(1-pertinencia)
                                 - (2-pertinencia)*e**(pertinencia-1)
                                 )
        if analise:
            figura, (plt1, plt2) = plt.subplots(1, 2)
          
            plt1.set_title("no background")
            plt1.plot(range(0,len(pertinencias_b)), pertinencias_b, color = 'b')
            plt1.axvline(mi_b)
            
            plt2.set_title("no foreground")
            plt2.plot(range(len(pertinencias_b), 256), pertinencias_f, color = 'b')
            plt2.axvline(mi_f)

            plt.suptitle("Distribuicoes de pertinencia, limiar=" + str(limiar))
            plt.show()
            
        return divergencia
    
    #Inicia a quantidade de pixels e soma das intensidades no back e foreground.
    limiar_inicial = 0 #ultima intensidade do background
    sum_intensidade_b = 0
    sum_intensidade_f = 0
    for intensidade in range(1, 256):
        sum_intensidade_f += intensidade*histograma[intensidade, 0]
    qtd_b = histograma[0, 0]
    qtd_f = histograma[:, 0].sum() - histograma[0, 0]
    if qtd_b == 0: #evita divisao por 0
        mi_b = 0
    else:
        mi_b = sum_intensidade_b/qtd_b
    if qtd_f == 0: #evita divisao por 0
        mi_f = 0
    else:
        mi_f = sum_intensidade_f/qtd_f
    
    #Inicia o limiar inicial como sendo o otimo, para futura comparacao.
    menor_divergencia = divergencia_fuzzy(limiar_inicial, mi_b, mi_f)
    melhor_limiar = limiar_inicial

    divergencias = [menor_divergencia]
    #Faz a busca linear pelo limiar que otimiza a divergencia fuzzy.
    for limiar in range(1, 255):
        #Modifica a quantidade de pixels e soma da intensidades no background
        #e foreground com base na quantidade de pixels mudando de regiao.
        qtd_mudando_regiao = histograma[limiar, 0]
        sum_intensidade_b += limiar*qtd_mudando_regiao
        sum_intensidade_f -= limiar*qtd_mudando_regiao
        qtd_b += qtd_mudando_regiao
        qtd_f -= qtd_mudando_regiao
        if qtd_b == 0: #evita divisao por 0
            mi_b = 0
        else:
            mi_b = sum_intensidade_b/qtd_b
        if qtd_f == 0: #evita divisao por 0
            mi_f = 0
        else:
            mi_f = sum_intensidade_f/qtd_f
            
        #Se essa opcao for melhor que a atualmente otima, a substitue.
        divergencia = divergencia_fuzzy(limiar, mi_b, mi_f,
                                        analise=((limiar-10)%50==0 and analise))
        if divergencia < menor_divergencia:
            menor_divergencia = divergencia
            melhor_limiar = limiar

        if analise:
            divergencias.append(divergencia)
        
    if analise:
        import numpy as np
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        #ax1.title("Histograma da imagem")
        ax1.plot(range(0, 256), histograma, color = 'b')
        ax1.axvline(melhor_limiar)
        div_norm = divergencias - np.min(divergencias)
        div_norm = div_norm/np.max(div_norm)
        div_norm = div_norm*np.max(histograma)
        ax1.plot(range(0, 256), 
                 np.concatenate((div_norm, np.array([div_norm[-1]]))),
                 color = 'r')
        #ax2.imshow(np.vstack((divergencias, divergencias)), aspect=1,
        #           norm=norm, cmap='coolwarm')
        plt.suptitle("Divergencias para cada limiar")
        plt.show()
                
        from scipy import stats
        print "Descricao das divergencias para cada limiar: " + str(stats.describe(divergencias))
        print "Limiar ganhador e sua divergencia associada: " + str((melhor_limiar, menor_divergencia))
        
    #Aplica o limiar otimo encontrado na limiarizacao
    segmentos = cv2.threshold(imagem, melhor_limiar, 255, cv2.THRESH_BINARY_INV)[1]
    if mascara is not None:
        segmentos = cv2.bitwise_and(segmentos, segmentos, mask=mascara)

    #Usa metade do limiar como instruido em Ghosh, 2010 para se encontrar os nucleos
    segmentos_div_2 = cv2.threshold(imagem, melhor_limiar/2, 255, cv2.THRESH_BINARY_INV)[1]
    if mascara is not None:
        segmentos_div_2 = cv2.bitwise_and(segmentos_div_2, segmentos_div_2, mask=mascara)
    
    if analise:
        mostra_imagens([segmentos, segmentos_div_2], "Imagens limiarizadas",
                       ["Limiar otimo", "Metade do limiar otimo"])
        
    return (melhor_limiar, segmentos, segmentos_div_2)
    #----- /Fuzzy Divergence -----

#Parser de parametros do script.
import argparse
parser = argparse.ArgumentParser(description="Limiarizacao por divergencia fuzzy.")
parser.add_argument("-i", "--input", help="Nome do arquivo da imagem de entrada.",
                    action="store")
parser.add_argument("-m", "--mask", 
                    help="Nome do arquivo da imagem binaria de mascara.", 
                    action="store")
parser.add_argument("-s", "--salvar", help="Nome do arquivo da imagem de saida.", 
                    action="store")
parser.add_argument("-a", "--analise", help="Modo de analise.",
                    action="store_true")
args = parser.parse_args()

#Abre a imagem de entrada e considera apenas o canal verde
input_filename = args.input
if input_filename is not None:
    imagem = cv2.imread(input_filename, cv2.IMREAD_COLOR)[:,:,1]
    
    if args.mask != None:
        mascara = cv2.imread(args.mask, cv2.IMREAD_GRAYSCALE)
    else: 
        mascara = None
            
    seg_1, seg_2 = limiarizacao_divergencia_fuzzy(imagem, mascara, 
                                                  gamma=30,
                                                  c=1,
                                                  analise=args.analise)
    
    #Se especificado, salva a imagem de saida
    if args.salvar != None:
        cv2.imwrite(args.salvar, seg_1)
        cv2.imwrite(args.salvar[:-4] + "_2" + args.salvar[-4:], seg_2)