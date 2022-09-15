import xml.etree.ElementTree as ET
import numpy as np


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

    def copiarAFD(self):

        AFD_Copia = AutomatoFD(self.alfabeto)
        AFD_Copia.estados = self.estados
        AFD_Copia.transicoes = self.transicoes
        AFD_Copia.inicial = self.inicial
        AFD_Copia.finais = self.finais
        AFD_Copia.funcao = self.funcao
        AFD_Copia.qtdEstados = self.qtdEstados
        AFD_Copia.qtdTransicoes = self.qtdTransicoes

        return AFD_Copia

    def guritimo_complemento(self):

        automato_comp = self.copiarAFD()

        for i in automato_comp.estados:
            if i in automato_comp.finais:
                automato_comp.mudaEstadoFinal(i,False)
            else:
                automato_comp.mudaEstadoFinal(i,True)
        return automato_comp

    def estadosEquivalentes(self):

        tblEq = self.obterTrivialmenteNaoEquivalentes()

        for i in range(2,len(self.estados)):
            for j in range(1,len(self.estados) - 1):
                if i == j:
                    break
                else:
                    for char in self.alfabeto:
                        qi = self.transicoes[(i,char)]
                        qj = self.transicoes[(j,char)]
                        print(f"Atuais: {i,j}, letra {char}, Destino: {qi,qj} ")

                        if qi != qj:
                            if tblEq[(qi,qj)] == False: #Sao trivialmente não equivalentes
                                print("marca false")
                                tblEq[(i,j)] = False
                                tblEq[(j,i)] = False
                                break
                            else: #Não sei
                                print("não sei, append")
                                tblEq[(qi,qj)].append((i,j))
                                tblEq[(qj,qi)].append((i,j))

        self.printTbl(tblEq,True)

    def printTbl(self,tblEq,printaSomenteEquivalentes):

        print("Tabela de Equivalencia")
        if printaSomenteEquivalentes:
            for i in range(2,len(self.estados)):
                print(f"{i}| ", end="")
                for j in range(1,len(self.estados) - 1):
                    if i == j:
                        break
                    else:
                        print(f"{tblEq[(i,j)]}, ", end="")
                print("\n")

    def obterTrivialmenteNaoEquivalentes(self):

        col = list(self.estados)
        lin = list(self.estados)

        col.remove(col[0])
        lin.remove(col[-1])

        tblEquiv = dict()

        for i in col:
            for j in lin:
                if i == j:
                    break
                else:
                    if self.trivialmenteNaoEquiv(i,j):
                        tblEquiv[(i,j)] = False
                        tblEquiv[(j,i)] = False
                    else:
                        tblEquiv[(i,j)] = []
                        tblEquiv[(j,i)] = []

        return tblEquiv

    def trivialmenteNaoEquiv(self, qj, qi):
        if qi in self.finais and qj in self.finais: #se forem finais
            return False
        if qi in self.finais and qj not in self.finais: #se i for final e j nao(nao equiv)
            return True
        if qi not in self.finais and qj in self.finais: #se j for final e i nao(nao equiv)
            return True
        if qi not in self.finais and qj not in self.finais: #se nenhum for final
            return False

    def __str__(self):
        s = 'AFD(Q, Σ, δ, q0, F): \n'
        s += 'Q = {'
        for a in self.alfabeto:
            s += "'{}', ".format(str(a))
        s += '} \n'
        s += 'Σ = {'
        for e in self.estados:
            s += '{}, '.format(str(e))
        s += '} \n'
        s += 'δ = {'
        for (e, a) in self.transicoes.keys():
            d = self.transicoes[(e, a)]
            s += "({},{})-->{}; ".format(e, a, d)
        s += ';} \n'
        s += 'q0 = {} \n'.format(self.inicial)
        s += 'F = {'
        for e in self.finais:
            s += '{}, '.format(str(e))
        s += '}'
        return s

    def salvarArquivo(self,nome):
        # salvando no modelo do JFLAP
        try:

            arqObj = open(nome + ".jff", "w")
            arqObj.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><structure>")
            arqObj.write("\n<type>fa</type>")  # automato finito
            arqObj.write("\n\t\t<automaton>")

            # Montagem AFD
            i = 1
            # Salvando os estados
            while True:

                if i == self.qtdEstados + 1:
                    break
                else:
                    arqObj.write("\n<state id=\"{}\" name =\"q{}\" >\n".format(i, i))
                    if i == self.inicial:  # verifica se o estado a ser salvo é inicial e salva
                        if i in self.finais: #se o estado inicial também for final
                            arqObj.write("<initial/>\n<final/>\n</state>")
                        else:
                            arqObj.write("<initial/>\n</state>")
                    elif i in self.finais:  # verifica se o estado a ser salvo é final e salva
                        arqObj.write("<final/>\n</state>")
                    else:
                        arqObj.write("</state>")
                i = i + 1

            # Salvando as transicoes
            i = 1

            #i = Estado atual
            #d = Proximo Estado
            #j = String lida

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




def importarAFD(diretorio):

    try:

        alfabeto = ''
        Estado = 1
        arq = open(diretorio,"r")
        raiz = ET.parse(arq).getroot()

        #obtendo o alfabeto
        for filho in raiz:
            for f in filho:
                if f.tag == 'transition':
                    # Calculando primeiro o alfabeto (sem ele, não é possivel realizar as transições)
                    for x in f:  # seleciona cada simbolo diferente do conjunto de transiçoes, motando o alfabeto
                        if x.tag == 'read':
                            if x.text is not None:
                                if x.text not in alfabeto:
                                    alfabeto += x.text

        # Cria o alfabeto
        AFD = AutomatoFD(alfabeto)

        Estado = 1
        #contando os estados
        for filho in raiz:
            for f in filho:
                if f.tag == 'state':
                    AFD.criaEstado(Estado)
                    Estado = Estado + 1

        Estado = 1
        #obtendo estados iniciais, finais e transicoes
        for filho in raiz:
            for f in filho:
                # conjunto de estados
                if f.tag == 'state':
                    for s in f:
                        if s.tag == 'initial':
                            AFD.mudaEstadoInicial(Estado)
                        if s.tag == 'final':
                            AFD.mudaEstadoFinal(Estado,True)

                    Estado = Estado + 1

                elif f.tag == 'transition':
                    origem = -1
                    simbolo = ''
                    destino = -1

                    #Transiçoes
                    for t in f:
                        if t.tag == 'from':
                            origem = int(t.text) + 1
                        elif t.tag == 'read':
                            if t.text is not None:
                                simbolo = t.text
                        elif t.tag == 'to':
                            destino = int(t.text) + 1

                    AFD.criaTransicao(origem, destino,simbolo)

        arq.close()
        #AFD.funcao = input("\nDefina a função do Automato: ")
        print("\nAFD importado com sucesso !")
        return AFD

    except Exception as Erro:
        print(Erro)