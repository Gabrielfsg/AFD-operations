from .Estrategia import Estrategia
from ..AutomatoFD import AutomatoFD
from ..Util.ConjuntosENUM import Conjunto

class Conjuntos(Estrategia):

    def __init__(self, afd1: AutomatoFD,tipoOp: Conjunto,afd2: AutomatoFD = None):
        self._afdN1 = afd1
        self._afdN2 = afd2
        self._tipoOp = tipoOp

    def operacao(self):

        if self._tipoOp == Conjunto.COMPLEMENTO:
            return self.complemento_automato()
        else:

            if self._afdN2 is None: #Não dá pra  multiplicar um automato com nada
                print("É necessário que seja passado um segundo autômato !")
                return

            afd_mult, estados = self.multiplicacao_automato()
            match self._tipoOp: #Verificando a operação desejada
                case Conjunto.MULTIPLICACAO:
                    return afd_mult
                case Conjunto.UNIAO:
                    return self.uniao_automato(afd_mult,estados)
                case Conjunto.INTERSECCAO:
                    return self.intersecao_automato(afd_mult,estados)
                case Conjunto.DIFERENCA:
                    return self.diferenca_automato(afd_mult,estados)
                case _:
                    return "Operação Não Reconhecida !"

    def multiplicacao_automato(self):
        estados = dict()
        automato_mult = AutomatoFD(self._afdN1.alfabeto)
        numA1 = len(self._afdN1.estados)
        numA2 = len(self._afdN2.estados)
        count = 1

        estadosTotaisMult = (numA1 * numA2) + 1  # numero máximo de estados criados

        for i in range(1, estadosTotaisMult):
            automato_mult.criaEstado(i)  ### cria novo automato com todos os estados

        for i in range(1, numA1 + 1):
            for p in range(1, numA2 + 1):
                estados[(i, p)] = count  ### cria um dicionario de tuplas com os estados novos com os antigos
                count += 1

        # print("ESTADOS: ", estados)
        # print(self.transicoes)
        # print(afdN2.transicoes)

        for i in range(1, numA1 + 1):
            for p in range(1, numA2 + 1):
                for l in list(self._afdN1.alfabeto):
                    automato_mult.criaTransicao(estados[(i, p)],
                                                estados[(self._afdN1.transicoes[(i, l)], self._afdN2.transicoes[(p, l)])],
                                                l)  # cria as transições dos estados do novo automato iterando pelo numero
                    # número de estados dos automatos multiplicados

        automato_mult.inicial = estados[(self._afdN1.inicial, self._afdN2.inicial)]
        return automato_mult, estados

    def intersecao_automato(self, automato_mult, estados):

        for i in self._afdN1.finais:
            for p in self._afdN2.finais:
                if ((i, p) in estados.keys()):
                    automato_mult.mudaEstadoFinal(estados[(i, p)],
                                                  True)  # se a tupla de estados finais exister no dicionario torna ela o estado final do novo automato

        # print(automato_mult)

        return automato_mult

    def uniao_automato(self,automato_mult, estados):

        for e in estados:
            for i in self._afdN1.finais:
                if (e[0] == i):
                    automato_mult.mudaEstadoFinal(estados[e],
                                                  True)  # Poe com estado final se algum elemento da tupla tem o estado de um dos automatos

            for p in self._afdN2.finais:
                if (e[1] == p):
                    automato_mult.mudaEstadoFinal(estados[e],
                                                  True)  # Poe com estado final se algum elemento da tupla tem o estado de um dos automatos

        return automato_mult

    def diferenca_automato(self, automato_mult, estados):

        automato_mult.inicial = estados[(self._afdN1.inicial, self._afdN2.inicial)]
        estadosFinais = dict()
        naoFinais = [estado for estado in self._afdN2.estados if estado not in self._afdN2.finais]
        count = 1
        for i in self._afdN1.finais:  # adiciona  ao dicionária de estados finais a tupla de final de um (A) com o não final de outro (B). Exemplo: A - B
            for p in naoFinais:
                estadosFinais[(i, p)] = count
                count += 1

        for p in estadosFinais:
            if (p in estados.keys()):
                automato_mult.mudaEstadoFinal(estados[p], True)

        # print("ESTADOS: ", estados)
        # print(self._afdN1.transicoes)
        # print(self._afdN2.transicoes)
        # print(naoFinais)
        # print(estadosFinais)
        return automato_mult

    def complemento_automato(self):

        automato_comp = self._afdN1.copiarAFD()

        for i in automato_comp.estados:
            if i in automato_comp.finais:
                automato_comp.mudaEstadoFinal(i, False)  # faz a troca dos estados finais para não finais
            else:
                automato_comp.mudaEstadoFinal(i, True)  # faz a troca dos estados não finais para finais
        return automato_comp



