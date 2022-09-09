class AutomatoFD:

    def __init__(self, Alfabeto):
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.inicial = None
        self.finais = set()
        self.funcao = None
        self.qtdEstados = 0
        self.qtdTransicoes = 0

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
        s = 'AFD(Q, Σ, δ, q0, F): \n'
        s += 'A = {'
        for a in self.alfabeto:
            s += "'{}', ".format(str(a))
        s += '} \n'
        s += 'E = {'
        for e in self.estados:
            s += '{}, '.format(str(e))
        s += '} \n'
        s += 'T = {'
        for (e, a) in self.transicoes.keys():
            d = self.transicoes[(e, a)]
            s += "({},{})-->{}; ".format(e, a, d)
        s += ';} \n'
        s += 'i = {} \n'.format(self.inicial)
        s += 'F = {'
        for e in self.finais:
            s += '{}, '.format(str(e))
        s += '}'
        return s

    def salvarArquivo(self, diretorio, nome):

        path = diretorio + '\\' + nome + '.jff'
        # salvando no modelo do JFLAP

        try:

            arqObj = open(path, "w")
            arqObj.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><structure>")
            arqObj.write("\n<type>fa</type>")  # automato finito
            arqObj.write("\n\t\t<automaton>")

            # Montagem AFD
            i = 1
            # Salvando os estados
            while True:

                if i == self.qtdEstados:
                    break
                else:
                    arqObj.write("\n<state id=\"{}\" name =\"q{}\" >\n".format(i, i))
                    if i == self.inicial:  # verifica se o estado a ser salvo é inicial e salva
                        arqObj.write("<initial/>\n</state>")
                    elif i in self.finais:  # verifica se o estado a ser salvo é final e salva
                        arqObj.write("<final/>\n</state>")
                    else:
                        arqObj.write("</state>")
                i = i + 1

            # Salvando as transicoes
            i = 1

            for (i, j) in self.transicoes.keys():
                d = self.transicoes[(i, j)]
                arqObj.write(
                    "\n<transition>\n\t<from>{}</from>\n\t<to>{}</to>\n\t<read>{}</read>\n\t</transition>".format(i, d, j))

            arqObj.write("\n\t</automaton>")
            arqObj.write("\n</structure>")

            arqObj.close()
            print("\nAFD salvo com sucesso !")
        except Exception as Erro:
            print("\nErro ao salvar o arquivo ! {}".format(Erro))
