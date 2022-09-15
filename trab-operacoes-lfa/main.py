from AutomatoFD import *

if __name__ == '__main__':

    afd = AutomatoFD('ab')

    #AFD Lista 1 Exercício 7 - nao contem bab e contem par de a
    for i in range(1, 9):
        afd.criaEstado(i)
        afd.qtdEstados = i

    afd.mudaEstadoInicial(1)
    afd.mudaEstadoFinal(1, True)
    afd.mudaEstadoFinal(2, True)
    afd.mudaEstadoFinal(3, True)

    afd.criaTransicao(1, 5, 'a')
    afd.criaTransicao(2, 7, 'a')
    afd.criaTransicao(3, 5, 'a')
    afd.criaTransicao(4, 8, 'a')
    afd.criaTransicao(5, 1, 'a')
    afd.criaTransicao(6, 3, 'a')
    afd.criaTransicao(7, 1, 'a')
    afd.criaTransicao(8, 4, 'a')
    afd.criaTransicao(1, 2, 'b')
    afd.criaTransicao(2, 2, 'b')
    afd.criaTransicao(3, 4, 'b')
    afd.criaTransicao(4, 4, 'b')
    afd.criaTransicao(5, 6, 'b')
    afd.criaTransicao(6, 6, 'b')
    afd.criaTransicao(7, 8, 'b')
    afd.criaTransicao(8, 8, 'b')
    afd.funcao = "nao contem bab e contem par de a"

    #print(afd.transicoes)

    #afd.salvarArquivo("AFDTeste")

    #print(afd)

    cadeia = 'abbabaabbbbbba'
    afd.limpaAfd()
    parada = afd.move(cadeia)
    if not afd.deuErro() and afd.estadoFinal(parada):
        print('Aceita cadeia "{}"'.format(cadeia))
    else:
        print('Rejeita cadeia "{}"'.format(cadeia))

    #print("###COMPLEMENTO###")
    #print(afd.guritimo_complemento())
    #print("###")

    #AFD_importado = importarAFD("AFDTeste.jff")
    #print("###Importando Automato...###")
    #print(AFD_importado)
    afd.estadosEquivalentes()

    #afd2 = importarAFD("AFDTeste2.jff")
    #print(afd2)
    #afd2.estadosEquivalentes()
