from .Estrategia import Estrategia
from ..AutomatoFD import AutomatoFD
from ..Util.Equivalencias import Equivalencias

class EquivalenciaAFDS(Estrategia):

    def __init__(self,afd1: AutomatoFD,afd2: AutomatoFD):
        self._afdN1 = afd1
        self._afdN2 = afd2

    def operacao(self):

        if self._afdN1.alfabeto != self._afdN2.alfabeto:
            return "O alfabeto deve ser o mesmo nos dois automatos."

        afdValidacao = AutomatoFD(self._afdN1.alfabeto)

        count = 1
        for i in self._afdN1.estados:
            afdValidacao.criaEstado(count)
            if i in self._afdN1.finais:
                afdValidacao.mudaEstadoFinal(count, True)
            count += 1

        for i in self._afdN2.estados:
            afdValidacao.criaEstado(count)
            if i in self._afdN2.finais:
                afdValidacao.mudaEstadoFinal(count, True)
            count += 1

        afdValidacao.mudaEstadoInicial(self._afdN1.inicial)
        tblEq = Equivalencias(afdValidacao).obterTrivialmenteNaoEquivalentes()
        # print(afdValidacao)
        # self.printTbl(tblEq)

        for i in afdValidacao.estados:
            for j in afdValidacao.estados:
                if i == j:
                    break
                else:
                    if tblEq[(i, j)] != False:
                        for char in self._afdN1.alfabeto:

                            if i <= len(self._afdN1.estados):
                                qi = self._afdN1.transicoes[(i, char)]
                            else:
                                qi = self._afdN2.transicoes[(i - len(self._afdN1.estados), char)] + len(self._afdN1.estados)

                            if j <= len(self._afdN1.estados):
                                qj = self._afdN1.transicoes[(j, char)]
                            else:
                                qj = self._afdN2.transicoes[(j - len(self._afdN1.estados), char)] + len(self._afdN1.estados)

                            # print(f"Atuais: {i,j}, letra {char}, Destino: {qi,qj} ")
                            # if qi != qj:  # nao analisa tuplas iguais
                            #     if tblEq[(qi, qj)] == False:  # Estados não equivalentes, logo, os AFDs nao sao equiv.
                            #         return "Os automatos nao são equivalentes"
                            # else:
                            tblEq[(i, j)].append((qi, qj))  # seta valores aos que podem ser  equivalente
                            tblEq[(j, i)].append((qi, qj))  # seta valores aos que podem ser  equivalente

        # Função que itera todos os estados da tabela de equivalência:
        # 1° Valida se o estado ta marcado como false. se não vai para a etapa 2 se sim passa para o próximo
        # 2° após isso ele itera a lista encadeada do estado que não está marcado como false
        # 3° se algum da lista encadeada estiver no dicionario como false, ele seta o estado como false e depois
        # itera toda a lista setando os estados que tem o estado que acabou de ser setado com false tbm

        for tup in tblEq:
            # print(f'tupla antes do for: {tup}')
            if (tblEq[tup] != False):
                for i in tblEq[tup]:
                    if (i in tblEq):
                        if (tblEq[i] == False):
                            tblEq[tup] = False
                            # print(tup)
                            for g in tblEq:
                                if (tblEq[g] != False):
                                    if (tup in tblEq[g]):
                                        tblEq[g] = False

        if tblEq[(self._afdN1.inicial,
                  len(self._afdN1.estados) + 1)] == False:  # verifica se o estado inicial do automato 1 e do 2 são ou não equivalentes
            print("Os automâtos não são equivalentes")
            return
        else:
            print("Os automâtos são equivalentes")
            return



