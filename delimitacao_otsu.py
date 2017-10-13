import cv2
import cv2.cv
import argparse
from exibir_imagens import mostra_imagens
    
def delimitacao_otsu(imagem, analise=False):
    if analise:
        print "- Delimitacao por limiarizacao de Otsu -"
        mostra_imagens([imagem], "", ["Imagem de entrada, apenas um canal"])
        
    #Binarizacao por Otsu
    limiar, binaria = cv2.threshold(imagem, 0, 255, 
                                    cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    if analise:
        mostra_imagens([binaria], "",
                       ["Imagem binaria limiarizada em " + str(limiar)])
        
    return binaria

#Parser de parametros do script
parser = argparse.ArgumentParser(description="Delimita a regiao circular da lamina.")
parser.add_argument("-i", "--input", help="Nome do arquivo da imagem de entrada.", action="store")
parser.add_argument("-s", "--salvar", help="Nome do arquivo da imagem de saida.", action="store")
parser.add_argument("-a", "--analise", help="Modo de analise.", action="store_true")
args = parser.parse_args()

#Abre a imagem de entrada e considera apenas o canal azul
input_filename = args.input
if input_filename is not None:
    imagem = cv2.imread(input_filename, cv2.IMREAD_COLOR)[:,:,0]

    binaria = delimitacao_otsu(imagem, args.analise)
    
    #Se especificado, salva a imagem de saida
    if args.salvar != None:
        cv2.imwrite(args.salvar, binaria)