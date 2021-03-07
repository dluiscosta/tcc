# Trabalho de Conclusão de Curso - Scripts Experimentais

Este repositório contém os *scripts* utilizados nos experimentos do meu trabalho de conclusão de curso de ciência da computação no [Centro Universitário da FEI](https://portal.fei.edu.br/), focado no uso de visão computacional e *machine learning* para automatizar exames diagnósticos.

Além da porção escrita do trabalho entregue à instituição, foi submetido um [paper](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwio3qjk9JzvAhXyL7kGHbrKCdIQFjADegQIBRAD&url=http%3A%2F%2Fsibgrapi.sid.inpe.br%2Farchive.cgi%2Fsid.inpe.br%2Fsibgrapi%2F2018%2F10.16.23.23&usg=AOvVaw3o6XCMUoINGT1JnW3Dxrap) ao SIBGRAPI 2017.

## Resumo do Trabalho

Segue o resumo original incluso no trabalho escrito:

> A contagem diferencial de leucócitos é importante para o diagnóstico de várias doenças.
> Quando feito manualmente, esse processo é lento e apresenta alta variância de resultados, além de requerer um especialista.
>
> Este trabalho propõe um método automático de contagem diferencial de neutrófilos e linfócitos a partir de imagens microscópicas.
> O método proposto é dividido em três etapas principais: pré-processamento, segmentação e reconhecimento dos leucócitos.
> Enquanto a segmentação é baseada em divergência *fuzzy* e contornos ativos duais, a classificação dos tipos de leucócitos, contida na etapa de reconhecimento, é feita por [máquinas de vetores de suporte](https://pt.wikipedia.org/wiki/M%C3%A1quina_de_vetores_de_suporte) (SVM).
>
> O método será validado sobre um banco de imagens proveniente de lavagens bronco-alveolares feitas em ratos de laboratório.
> As imagens são capturadas por meio de um microscópio de baixo custo e com o uso de um aparelho celular, o que testará a acessibilidade do método.

## Nota sobre o código

Os *scripts* presentes aqui foram escritos para serem executados apenas algumas vezes, tendo como único objetivo a geração de resultados para os experimentos.
Portanto, em maior parte, não foram levadas em consideração "boas" práticas de programação que, em outras circunstâncias, visariam por facilidade de manutenção, extensibilidade ou mesmo performance.
