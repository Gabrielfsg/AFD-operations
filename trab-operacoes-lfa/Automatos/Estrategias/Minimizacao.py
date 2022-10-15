from .Estrategia import Estrategia
from ..AutomatoFD import AutomatoFD
from ..Util.Equivalencias import Equivalencias

class Minimizacao(Estrategia):

    def __init__(self, afd: AutomatoFD):
        self._afd = afd

    def operacao(self):

        self.removerEstadosSemAlcance()

        estadosEquivalentes = Equivalencias(self._afd).estadosEquivalentes()
        # print(f"estados equivalentes: {estadosEquivalentes}")

        eliminar = dict()

        # quem joga pra aquele estado, agora vai jogar pro seu equivalente
        for par in estadosEquivalentes:
            # print(par)
            qi, qj = par
            if qj in eliminar.keys():  # Se o estado a ser eliminado ja foi eliminado
                qj = eliminar[qj]  # Obtenho o equivalente dele
                # print(f"par alterou pra: {qi,qj}")

            if qi != qj:  # Desnecessario analisar a equivalencia de um estado com ele mesmo

                for char in self._afd.alfabeto:
                    for e in self._afd.estados:
                        if self._afd.transicoes[(e, char)] == qj:  # encontra transições onde apareça o estado qj
                            self._afd.transicoes[(e, char)] = qi  # qi receberá o que antes entrava em qj
                            # print(f"{e, char} -> {self.transicoes[(e, char)]}, agora vai pra {qi}")

                if qj not in eliminar:
                    eliminar[qj] = qi
                    # print(f'colocou {qj} na lista de eliminados, ele é equivalente ao {qi}')

        # Excluindo estados e transições
        for e in eliminar.keys():
            for char in self._afd.alfabeto:
                self._afd.transicoes.pop((e, char))

            if e == self._afd.inicial: #Se o estado a ser removido for inicial, o equivalente dele passa a ser inicial
                self._afd.mudaEstadoInicial(eliminar[e])
            self._afd.estados.remove(e)

        return self._afd

    def removerEstadosSemAlcance(self):

        visitados = []
        fila = [self._afd.inicial]

        while fila:
            estado = fila.pop(0)
            # print(f"estado sendo explorado: {estado}")
            if estado not in visitados:
                visitados.append(estado)
                # olhando as transições
                try:
                    for char in self._afd.alfabeto:
                        # print(f"add estados novos pra explorar: {estado,char} --> {self.transicoes[(estado,char)]}")
                        fila.append(self._afd.transicoes[(estado, char)])
                except Exception:
                    pass

        # print(f"visitados: {visitados}")
        if (len(visitados) < len(self._afd.estados)):
            print("\nAtenção: foram encontrados estados inalcançáveis, os mesmos serão removidos")
            for i in list(self._afd.estados):
                if i not in visitados:
                    for char in self._afd.alfabeto:
                        del self._afd.transicoes[(i, char)]
                    self._afd.estados.remove(i)


