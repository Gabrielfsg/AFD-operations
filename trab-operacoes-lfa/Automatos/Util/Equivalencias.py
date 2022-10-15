from ..AutomatoFD import AutomatoFD

class Equivalencias():

    def __init__(self,afd: AutomatoFD):
        self._afd = afd

    def estadosEquivalentes(self):

        tblEq = self.obterTrivialmenteNaoEquivalentes()
        try:
            for i in self._afd.estados:
                for j in self._afd.estados:
                    if i == j:
                        break
                    else:
                        if tblEq[(i, j)] is not False and tblEq[(i, j)] is not None:
                            for char in self._afd.alfabeto:
                                qi = self._afd.transicoes[(i, char)]
                                qj = self._afd.transicoes[(j, char)]
                                # print(f"Atuais: {i,j}, letra {char}, Destino: {qi,qj} ")
                                if qi != qj:  # nao analisa tuplas iguais
                                    if tblEq[(qi, qj)] == False:  # Sao trivialmente não equivalentes
                                        # print("marca false")
                                        if len(tblEq[(i, j)]) > 0:
                                            tblEq = self.marcarLembretes(tblEq, i, j)
                                        tblEq[(i, j)] = False
                                        tblEq[(j, i)] = False
                                        break
                                    else:  # Não sei
                                        # print("não sei, append")
                                        if (i, j) not in tblEq[(qi, qj)]:  # lembrete repetido não entra
                                            tblEq[(qi, qj)].append((i, j))
                                            tblEq[(qj, qi)].append((i, j))

            # Percorrendo novamente o dicionário para obter os estados Equivalentes
            equivalentes = []
            for i in self._afd.estados:
                for j in self._afd.estados:
                    if i == j:
                        break
                    else:
                        if tblEq[(i, j)] is not False and tblEq[(i, j)] is not None:
                            equivalentes.append((i, j))

            return equivalentes

        except Exception as erro:
            print("Erro ao minimizar automato, verifique se o mesmo não contem estados com transições incompletas")
            print(f'Descrição do erro: {erro}')

    def marcarLembretes(self, tblEq, i, j):
        lista = tblEq[(i, j)]
        # print(f"lembrete no {i,j}: {lista}")

        if lista:
            for tupla in lista:
                tblEq[(i, j)].remove(tupla)
                qi, qj = tupla
                # print(f"while lembrete: {qi, qj}")
                t = tblEq[(qi, qj)]
                if type(t) is list:
                    if len(t) > 0:
                        tblEq = self.marcarLembretes(tblEq, qi, qj)
                    # print(f"marcando {qi,qj} como false")
                    tblEq[(qi, qj)] = False
                    tblEq[(qj, qi)] = False

        return tblEq

    def printTbl(self, tblEq):
        print("Tabela de Equivalencia")

        for i in self._afd.estados:
            print(f"{i}| ", end="")
            for j in self._afd.estados:
                if i == j:
                    break
                else:
                    print(f"{tblEq[(i, j)]}, ", end="")
            print("\n")

    def obterTrivialmenteNaoEquivalentes(self):
        tblEquiv = dict()

        for i in self._afd.estados:
            for j in self._afd.estados:
                if i == j:
                    break
                else:
                    if self.trivialmenteNaoEquiv(i, j):
                        tblEquiv[(i, j)] = False
                        tblEquiv[(j, i)] = False
                    else:
                        tblEquiv[(i, j)] = []
                        tblEquiv[(j, i)] = []

        # self.printTbl(tblEquiv)
        return tblEquiv

    def trivialmenteNaoEquiv(self, qj, qi):
        if qi in self._afd.finais and qj in self._afd.finais:  # se forem finais
            return False
        if qi in self._afd.finais and qj not in self._afd.finais:  # se i for final e j nao(nao equiv)
            return True
        if qi not in self._afd.finais and qj in self._afd.finais:  # se j for final e i nao(nao equiv)
            return True
        if qi not in self._afd.finais and qj not in self._afd.finais:  # se nenhum for final
            return False

