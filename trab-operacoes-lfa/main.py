from Automatos.AutomatoFD import AutomatoFD
from Automatos.Util.ConjuntosENUM import Conjunto

from Automatos.Estrategias.Contexto import Contexto
from Automatos.Estrategias.LerAFD import LerAFD
from Automatos.Estrategias.SalvarAFD import SalvarAFD
from Automatos.Estrategias.Conjuntos import Conjuntos
from Automatos.Estrategias.Minimizacao import Minimizacao
from Automatos.Estrategias.EquivalenciaAFDs import EquivalenciaAFDS

if __name__ == '__main__':

    afd = AutomatoFD('ab')

    # AFD Lista 1 Exercício 7 - nao contem bab e contem par de a
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

    # cadeia = 'abbabaabbbbbba'
    # afd.limpaAfd()
    # parada = afd.move(cadeia)
    # if not afd.deuErro() and afd.estadoFinal(parada):
    #     print('Aceita cadeia "{}"'.format(cadeia))
    # else:
    #     print('Rejeita cadeia "{}"'.format(cadeia))

    # Objeto que definirá a estrategia a ser utilizada pro automato
    contexto = Contexto()

    print("\n###OPERAÇÕES DE CONJUNTOS###")
    # print("\nComplemento AFD")
    #
    # contexto.estrategia = LerAFD('Automatos_Para_Teste/prefixo_ab-sufixo_ab.jff')
    # AFD = contexto.executarOperacao()
    #
    # contexto.estrategia = SalvarAFD(AFD,'afdsufix_ab_prefix_ab')
    # contexto.executarOperacao()
    #
    # contexto.estrategia = Conjuntos(AFD,Conjunto.COMPLEMENTO)
    # AFD = contexto.executarOperacao()
    #
    # contexto.estrategia = SalvarAFD(AFD,'afdsufix_ab_prefix_ab_complemento')
    # contexto.executarOperacao()

    # Criando dois novos automatos para teste (multiplicação,uniao,intersecção e diferença)
    # afdM1 = AutomatoFD('ab');
    # afdM2 = AutomatoFD('ab');
    #
    # for i in range(1, 5):
    #     afdM1.criaEstado(i)
    #
    # for i in range(1, 3):
    #     afdM2.criaEstado(i)
    #
    # afdM1.criaTransicao(1, 2, 'b')
    # afdM1.criaTransicao(1, 1, 'a')
    # afdM1.criaTransicao(2, 2, 'b')
    # afdM1.criaTransicao(2, 3, 'a')
    # afdM1.criaTransicao(3, 4, 'b')
    # afdM1.criaTransicao(3, 1, 'a')
    # afdM1.criaTransicao(4, 4, 'a')
    # afdM1.criaTransicao(4, 4, 'b')
    #
    # afdM2.criaTransicao(1, 1, 'b')
    # afdM2.criaTransicao(1, 2, 'a')
    # afdM2.criaTransicao(2, 2, 'b')
    # afdM2.criaTransicao(2, 1, 'a')
    #
    # afdM1.mudaEstadoInicial(1)
    # afdM2.mudaEstadoInicial(1)
    #
    # afdM2.mudaEstadoFinal(1, True)
    # afdM1.mudaEstadoFinal(1, True)
    # afdM1.mudaEstadoFinal(2, True)
    # afdM1.mudaEstadoFinal(3, True)
    #
    # print("\n###Automato M1###")
    # print(afdM1)
    # print("\n###Automato M2###")
    # print(afdM2)
    #
    # contexto.estrategia = SalvarAFD(afdM1, 'AFD_M1')
    # contexto.executarOperacao()
    #
    # contexto.estrategia = SalvarAFD(afdM2, 'AFD_M2')
    # contexto.executarOperacao()
    #
    # print("\n ###MULTIPLICAÇÃO###")
    #
    # contexto.estrategia = Conjuntos(afdM1,Conjunto.MULTIPLICACAO,afdM2)
    # AFD_Mult = contexto.executarOperacao()
    #
    # contexto.estrategia = SalvarAFD(AFD_Mult,'AFD_Mult')
    # contexto.executarOperacao()
    #
    # print(AFD_Mult)
    #
    # print("\n ###UNIÃO###")
    #
    # contexto.estrategia = Conjuntos(afdM1,Conjunto.UNIAO,afdM2)
    # AFD_Uniao = contexto.executarOperacao()
    #
    # contexto.estrategia = SalvarAFD(AFD_Uniao,'AFD_Uniao')
    # contexto.executarOperacao()
    #
    # print(AFD_Uniao)
    #
    # print("\n ###INTERSECÇÃO###")
    #
    # contexto.estrategia = Conjuntos(afdM1,Conjunto.INTERSECCAO,afdM2)
    # AFD_INTER = contexto.executarOperacao()
    #
    # contexto.estrategia = SalvarAFD(AFD_INTER,'AFD_INTER')
    # contexto.executarOperacao()
    #
    # print(AFD_INTER)
    #
    # print("\n ###DIFERENÇA###")
    #
    # contexto.estrategia = Conjuntos(afdM1,Conjunto.DIFERENCA,afdM2)
    # AFD_DIFF = contexto.executarOperacao()
    #
    # contexto.estrategia = SalvarAFD(AFD_DIFF,'AFD_DIFF')
    # contexto.executarOperacao()
    #
    # print(AFD_DIFF)

    print("\n ###MINIMIZAÇÃO DE AUTOMATOS###")

    # print("\nAutomato 1")
    #
    # print(afd)
    # contexto.estrategia = SalvarAFD(afd, 'afd')
    # contexto.executarOperacao()
    #
    # contexto.estrategia = Minimizacao(afd)
    # afdMin = contexto.executarOperacao()
    #
    # print("\nAutomato depois de minimizar")
    # print(afdMin)
    # contexto.estrategia = SalvarAFD(afdMin,'afdMin')
    # contexto.executarOperacao()

    # print("\nAutomato 2")

    # contexto.estrategia = LerAFD("Automatos_Para_Teste/prefixo_ab-sufixo_ab.jff")
    # afd2 = contexto.executarOperacao()
    #
    # print(afd2)
    # contexto.estrategia = SalvarAFD(afd2, 'afd2')
    # contexto.executarOperacao()
    #
    # contexto.estrategia = Minimizacao(afd2)
    # afd2Min = contexto.executarOperacao()
    #
    # print("\nAutomato depois de minimizar")
    # print(afd2Min)
    # contexto.estrategia = SalvarAFD(afd2Min, 'afd2Min')
    # contexto.executarOperacao()

    # print("\nAutomato 3 - DESCONEXO")

    # contexto.estrategia = LerAFD("Automatos_Para_Teste/AFDDESCONEXO.jff")
    # afd3 = contexto.executarOperacao()
    #
    # print(afd3)
    # contexto.estrategia = SalvarAFD(afd3, 'afd3')
    # contexto.executarOperacao()
    #
    # contexto.estrategia = Minimizacao(afd3)
    # afd3Min = contexto.executarOperacao()
    #
    # print("\nAutomato depois de minimizar")
    # print(afd3Min)
    # contexto.estrategia = SalvarAFD(afd3Min, 'afd3Min')
    # contexto.executarOperacao()

    # print("\nAutomato 4")

    # contexto.estrategia = LerAFD("Automatos_Para_Teste/AFDPROVA1.jff")
    # afd4 = contexto.executarOperacao()
    #
    # print(afd4)
    # contexto.estrategia = SalvarAFD(afd4, 'afd4')
    # contexto.executarOperacao()
    #
    # contexto.estrategia = Minimizacao(afd4)
    # afd4Min = contexto.executarOperacao()
    #
    # print("\nAutomato depois de minimizar")
    # print(afd4Min)
    # contexto.estrategia = SalvarAFD(afd4Min, 'afd4Min')
    # contexto.executarOperacao()

    # Criando mais dois automatos para testar as equivalencias
    # afdM3 = AutomatoFD('ab');
    # afdM4 = AutomatoFD('ab');
    #
    # for i in range(1, 4):
    #     afdM3.criaEstado(i)
    #
    # for i in range(1, 3):
    #     afdM4.criaEstado(i)
    #
    # afdM3.criaTransicao(1, 2, 'b')
    # afdM3.criaTransicao(1, 3, 'a')
    # afdM3.criaTransicao(2, 2, 'b')
    # afdM3.criaTransicao(2, 1, 'a')
    # afdM3.criaTransicao(3, 2, 'b')
    # afdM3.criaTransicao(3, 3, 'a')
    #
    # afdM3.criaTransicao(1, 1, 'b')
    # afdM3.criaTransicao(1, 2, 'a')
    # afdM3.criaTransicao(2, 2, 'b')
    # afdM3.criaTransicao(2, 1, 'a')
    #
    # afdM4.criaTransicao(1, 1, 'b')
    # afdM4.criaTransicao(1, 2, 'a')
    # afdM4.criaTransicao(2, 2, 'b')
    # afdM4.criaTransicao(2, 1, 'a')
    #
    # afdM3.mudaEstadoInicial(1)
    # afdM4.mudaEstadoInicial(1)
    #
    # afdM3.mudaEstadoFinal(2, True)
    # afdM4.mudaEstadoFinal(2, True)
    #
    # print(afdM3)
    # print(afdM4)
    #
    # contexto.estrategia = SalvarAFD(afdM3, 'afdM3')
    # contexto.executarOperacao()
    # contexto.estrategia = SalvarAFD(afdM4, 'afdM4')
    # contexto.executarOperacao()
    #
    print("\n###EQUIVALENCIA DE AUTOMATOS###")
    #
    # contexto.estrategia = EquivalenciaAFDS(afdM3, afdM4)
    # contexto.executarOperacao()











