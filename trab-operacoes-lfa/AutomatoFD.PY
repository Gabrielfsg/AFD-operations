class AutomatoFD:

    def __init__(self, Alfabeto):
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.inicial = None
        self.finais = set()

    def limpaAfd(self):
        self.__deuErro = False
        self.__estadoAtual = self.inicial

    def criaEstado(self, id, inicial=False, final=False):
        id = int(id)
        if id in self.estados:
            return False
        self.estados = self.estados.union({id})
        if inicial:
            self.inicial = id
        if final:
            self.finais = self.finais.union({id})
        return True

    def criaTransicao(self, origem, destino, simbolo):
        origem = int(origem)
        destino = int(destino)
        simbolo = str(simbolo)
        if not origem in self.estados:
            return False
        if not destino in self.estados:
            return False
        if len(simbolo) != 1 or not simbolo in self.alfabeto:
            return False
        self.transicoes[(origem, simbolo)] = destino
        return True

    def mudaEstadoInicial(self, id):
        if not id in self.estados:
            return
        self.inicial = id

    def mudaEstadoFinal(self, id, final):
        if not id in self.estados:
            return
        if final:
            self.finais = self.finais.union({id})
        else:
            self.finais = self.finais.difference({id})

    def move(self, cadeia):
        for simbolo in cadeia:
            if not simbolo in self.alfabeto:
                self.__deuErro = True
                break
            if (self.__estadoAtual, simbolo) in self.transicoes.keys():
                novoEstado = self.transicoes[(self.__estadoAtual, simbolo)]
                self.__estadoAtual = novoEstado
            else:
                self.__deuErro = True
                break
            return self.__estadoAtual

    def deuErro(self):
        return self.__deuErro

    def estadoAtual(self):
        return self.__estadoAtual

    def estadoFinal(self, id):
        return id in self.finais

    def __str__(self):
        s = 'AFD(A, E, T, i, F): \n'
        s += 'A = {'
        for a in self.alfabeto:
            s += "'{}', ".format(str(a))
        s += '} \n'
        s += 'E = {'
        for e in self.estados:
            s += '{}'.format(str(e))
        s += '} \n'
        s += 'T = {'
        for (e, a) in self.transicoes.keys():
            d = self.transicoes[(e, a)]
            s += ";({},{})-->{}".format(e, a, d)
        s += ';} \n'
        s += 'i = {} \n'.format(self.inicial)
        s += 'F = {'
        for e in self.finais:
            s += '{}, '.format(str(e))
        s += '}'
        return s


if __name__ == '__main__':

    afd = AutomatoFD('ab')

    for i in range(1, 9):
        afd.criaEstado(i)
    afd.mudaEstadoInicial(1)
    afd.mudaEstadoFinal(4, True)

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


    print(afd)

    cadeia = 'abbabaabbbbbba'
    afd.limpaAfd()
    parada = afd.move(cadeia)
    if not afd.deuErro() and afd.estadoFinal(parada):
        print('Aceita cadeia "{}"'.format(cadeia))
    else:
        print('Rejeita cadeia "{}"'.format(cadeia))
