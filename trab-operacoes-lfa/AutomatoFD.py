import xml.etree.ElementTree as ET
import os, threading


class AutomatoFD:

    def __init__(self, Alfabeto):
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.inicial = None
        self.finais = set()
        self.funcao = None

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

        return AFD_Copia

    def automatoEquivalentes(self, afd2):

        if (self.alfabeto != afd2.alfabeto):
            return "O alfabeto deve ser o mesmo nos dois automatos."

        afdValidacao = AutomatoFD(self.alfabeto)
        # nas linhas a seguir cria um automato fictício onde metade para baixo dos estados pertence ao primeiro automato e metade para cima ao segundo automato.
        count = 1
        for i in self.estados:
            afdValidacao.criaEstado(count)
            if i in self.finais:
                afdValidacao.mudaEstadoFinal(count, True)
            count += 1

        for i in afd2.estados:
            afdValidacao.criaEstado(count)
            if i in afd2.finais:
                afdValidacao.mudaEstadoFinal(count, True)
            count += 1

        afdValidacao.mudaEstadoInicial(self.inicial)
        tblEq = afdValidacao.obterTrivialmenteNaoEquivalentes()
        # print(afdValidacao)
        # self.printTbl(tblEq)

        for i in afdValidacao.estados:
            for j in afdValidacao.estados:
                if i == j:
                    break
                else:
                    if tblEq[(i, j)] != False:
                        for char in self.alfabeto:

                            if i <= len(self.estados):
                                qi = self.transicoes[(i, char)]
                            else:
                                qi = afd2.transicoes[(i - len(self.estados), char)] + len(self.estados)

                            if j <= len(self.estados):
                                qj = self.transicoes[(j, char)]
                            else:
                                qj = afd2.transicoes[(j - len(self.estados), char)] + len(self.estados)

                            # print(f"Atuais: {i,j}, letra {char}, Destino: {qi,qj} ")
                            # if qi != qj:  # nao analisa tuplas iguais
                            #     if tblEq[(qi, qj)] == False:  # Estados não equivalentes, logo, os AFDs nao sao equiv.
                            #         return "Os automatos nao são equivalentes"
                            # else:
                            tblEq[(i, j)].append((qi, qj))#seta valores aos que podem ser  equivalente
                            tblEq[(j, i)].append((qi, qj))#seta valores aos que podem ser  equivalente

        # Função que itera todos os estados da tabela de equivalência:
        # 1° Valida se o estado ta marcado como false. se não vai para a etapa 2 se sim passa para o próximo
        # 2° após isso ele itera a lista encadeada do estado que não está marcado como false
        # 3° se algum da lista encadeada estiver no dicionario como false, ele seta o estado como false e depois
        # itera toda a lista setando os estados que tem o estado que acabou de ser setado com false tbm

        for tup in tblEq:
            print(f'tupla antes do for: {tup}')
            if (tblEq[tup] != False):
                for i in tblEq[tup]:
                    if (i in tblEq):
                        if (tblEq[i] == False):
                            tblEq[tup] = False
                            print(tup)
                            for g in tblEq:
                                if (tblEq[g] != False):
                                    if (tup in tblEq[g]):
                                        tblEq[g] = False

        if tblEq[(self.inicial, len(self.estados) + 1)] == False:  # verifica se o estado inicial do automato 1 e do 2 são ou não equivalentes
            return "Os automatos nao são equivalentes"
        else:
            return "Os automatos sao equivalentes"

    def multiplicacao_automato(self, afdN2):
        estados = dict()
        automato_mult = AutomatoFD(self.alfabeto)
        numA1 = len(self.estados)
        numA2 = len(afdN2.estados)
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
                for l in list(self.alfabeto):
                    automato_mult.criaTransicao(estados[(i, p)],
                                                estados[(self.transicoes[(i, l)], afdN2.transicoes[(p, l)])],
                                                l)  # cria as transições dos estados do novo automato iterando pelo numero
                    # número de estados dos automatos multiplicados

        automato_mult.inicial = estados[(self.inicial, afdN2.inicial)]
        return automato_mult, estados

    def intersecao_automato(self, afdN2, automato_mult, estados):

        for i in self.finais:
            for p in afdN2.finais:
                if ((i, p) in estados.keys()):
                    automato_mult.mudaEstadoFinal(estados[(i, p)],
                                                  True)  # se a tupla de estados finais exister no dicionario torna ela o estado final do novo automato

        # print(automato_mult)

        return automato_mult

    def uniao_automato(self, afdN2, automato_mult, estados):

        for e in estados:
            for i in self.finais:
                if (e[0] == i):
                    automato_mult.mudaEstadoFinal(estados[e],
                                                  True)  # Poe com estado final se algum elemento da tupla tem o estado de um dos automatos

            for p in afdN2.finais:
                if (e[1] == p):
                    automato_mult.mudaEstadoFinal(estados[e],
                                                  True)  # Poe com estado final se algum elemento da tupla tem o estado de um dos automatos

        return automato_mult

    def diferenca_automato(self, afdN2, automato_mult, estados):

        automato_mult.inicial = estados[(self.inicial, afdN2.inicial)]
        estadosFinais = dict()
        naoFinais = [estado for estado in afdN2.estados if estado not in afdN2.finais]
        count = 1
        for i in self.finais:  # adiciona  ao dicionária de estados finais a tupla de final de um (A) com o não final de outro (B). Exemplo: A - B
            for p in naoFinais:
                estadosFinais[(i, p)] = count
                count += 1

        for p in estadosFinais:
            if (p in estados.keys()):
                automato_mult.mudaEstadoFinal(estados[p], True)

        print("ESTADOS: ", estados)
        print(self.transicoes)
        print(afdN2.transicoes)
        print(naoFinais)
        print(estadosFinais)
        return automato_mult

    def complemento_automato(self):

        automato_comp = self.copiarAFD()

        for i in automato_comp.estados:
            if i in automato_comp.finais:
                automato_comp.mudaEstadoFinal(i, False)  # faz a troca dos estados finais para não finais
            else:
                automato_comp.mudaEstadoFinal(i, True)  # faz a troca dos estados não finais para finais
        return automato_comp

    def automatoMinimo(self):

        self.removerEstadosSemAlcance()

        estadosEquivalentes = self.estadosEquivalentes()

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

                for char in self.alfabeto:
                    for e in self.estados:
                        if self.transicoes[(e, char)] == qj:  # encontra transições onde apareça o estado qj
                            self.transicoes[(e, char)] = qi  # qi receberá o que antes entrava em qj
                            # print(f"{e, char} -> {self.transicoes[(e, char)]}, agora vai pra {qi}")

                if qj not in eliminar:
                    eliminar[qj] = qi
                    # print(f'colocou {qj} na lista de eliminados, ele é equivalente ao {qi}')

        # Excluindo estados e transições
        for e in eliminar.keys():
            for char in self.alfabeto:
                self.transicoes.pop((e, char))

            if e == self.inicial: #Se o estado a ser removido for inicial, o equivalente dele passa a ser inicial
                self.mudaEstadoInicial(eliminar[e])
            self.estados.remove(e)

    def removerEstadosSemAlcance(self):

        visitados = []
        fila = [self.inicial]

        while fila:
            estado = fila.pop(0)
            # print(f"estado sendo explorado: {estado}")
            if estado not in visitados:
                visitados.append(estado)
                # olhando as transições
                try:
                    for char in self.alfabeto:
                        # print(f"add estados novos pra explorar: {estado,char} --> {self.transicoes[(estado,char)]}")
                        fila.append(self.transicoes[(estado, char)])
                except Exception:
                    pass

        # print(f"visitados: {visitados}")

        if (len(visitados) < len(self.estados)):
            print("\nAtenção: foram encontrados estados inalcançáveis, os mesmos serão removidos")
            for i in list(self.estados):
                if i not in visitados:
                    for char in self.alfabeto:
                        del self.transicoes[(i, char)]
                    self.estados.remove(i)

    def estadosEquivalentes(self):

        tblEq = self.obterTrivialmenteNaoEquivalentes()

        try:
            for i in self.estados:
                for j in self.estados:
                    if i == j:
                        break
                    else:
                        if tblEq[(i, j)] is not False and tblEq[(i, j)] is not None:
                            for char in self.alfabeto:
                                qi = self.transicoes[(i, char)]
                                qj = self.transicoes[(j, char)]
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
            for i in self.estados:
                for j in self.estados:
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

        for i in self.estados:
            print(f"{i}| ", end="")
            for j in self.estados:
                if i == j:
                    break
                else:
                    print(f"{tblEq[(i, j)]}, ", end="")
            print("\n")

    def obterTrivialmenteNaoEquivalentes(self):

        tblEquiv = dict()

        for i in self.estados:
            for j in self.estados:
                if i == j:
                    break
                else:
                    if self.trivialmenteNaoEquiv(i, j):
                        tblEquiv[(i, j)] = False
                        tblEquiv[(j, i)] = False
                    else:
                        tblEquiv[(i, j)] = []
                        tblEquiv[(j, i)] = []

        self.printTbl(tblEquiv)
        return tblEquiv

    def trivialmenteNaoEquiv(self, qj, qi):
        if qi in self.finais and qj in self.finais:  # se forem finais
            return False
        if qi in self.finais and qj not in self.finais:  # se i for final e j nao(nao equiv)
            return True
        if qi not in self.finais and qj in self.finais:  # se j for final e i nao(nao equiv)
            return True
        if qi not in self.finais and qj not in self.finais:  # se nenhum for final
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

    def salvarArquivo(self, nome):
        # salvando no modelo do JFLAP
        try:

            arqObj = open(nome + ".jff", "w")
            arqObj.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><structure>")
            arqObj.write("\n<type>fa</type>")  # automato finito
            arqObj.write("\n\t\t<automaton>")

            # Montagem AFD
            # Salvando os estados
            for i in self.estados:

                arqObj.write("\n<state id=\"{}\" name =\"q{}\" >\n".format(i, i))
                if i == self.inicial:  # verifica se o estado a ser salvo é inicial e salva
                    if i in self.finais:  # se o estado inicial também for final
                        arqObj.write("<initial/>\n<final/>\n</state>")
                    else:
                        arqObj.write("<initial/>\n</state>")
                elif i in self.finais:  # verifica se o estado a ser salvo é final e salva
                    arqObj.write("<final/>\n</state>")
                else:
                    arqObj.write("</state>")

            # Salvando as transicoes
            # i = Estado atual
            # d = Proximo Estado
            # j = String lida

            for (i, j) in self.transicoes.keys():
                d = self.transicoes[(i, j)]
                arqObj.write(
                    "\n<transition>\n\t<from>{}</from>\n\t<to>{}</to>\n\t<read>{}</read>\n\t</transition>".format(i, d,
                                                                                                                  j))

            arqObj.write("\n\t</automaton>")
            arqObj.write("\n</structure>")
            arqObj.close()

            threading.Thread(target=abrirJFLAP, args=(nome,)).start()

            print("\nAFD salvo com sucesso !")
        except Exception as Erro:
            print("\nErro ao salvar o arquivo ! {}".format(Erro))


def abrirJFLAP(nomeArq):
    os.system(f'cmd /k "java -jar JFLAP7.1.jar {nomeArq}.jff"')


def importarAFD(diretorio):
    try:

        alfabeto = ''
        Estado = 1
        arq = open(diretorio, "r")
        raiz = ET.parse(arq).getroot()

        # obtendo o alfabeto
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

        # contando os estados
        for filho in raiz:
            for f in filho:
                if f.tag == 'state':
                    e = int(f.attrib['id'])
                    AFD.criaEstado(e)
                    for s in f:
                        if s.tag == 'initial':
                            AFD.mudaEstadoInicial(e)
                        if s.tag == 'final':
                            AFD.mudaEstadoFinal(e, True)

                elif f.tag == 'transition':

                    origem = -1
                    simbolo = ''
                    destino = -1

                    # Transiçoes
                    for t in f:
                        if t.tag == 'from':
                            origem = int(t.text)
                        elif t.tag == 'read':
                            if t.text is not None:
                                simbolo = t.text
                        elif t.tag == 'to':
                            destino = int(t.text)

                    AFD.criaTransicao(origem, destino, simbolo)

        arq.close()
        # AFD.funcao = input("\nDefina a função do Automato: ")
        print("\nAFD importado com sucesso !")
        return AFD

    except Exception as Erro:
        print(Erro)
