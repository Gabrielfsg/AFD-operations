import os
import threading
from .Estrategia import Estrategia
from ..AutomatoFD import AutomatoFD

class SalvarAFD(Estrategia):

    def __init__(self,afd: AutomatoFD, nomeArq):
        self._afd = afd
        self._nomeArq = nomeArq

    def operacao(self):

        # salvando no modelo do JFLAP
        try:

            arqObj = open(self._nomeArq + ".jff", "w")
            arqObj.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><structure>")
            arqObj.write("\n<type>fa</type>")  # automato finito
            arqObj.write("\n\t\t<automaton>")

            # Montagem AFD
            # Salvando os estados
            for i in self._afd.estados:

                arqObj.write("\n<state id=\"{}\" name =\"q{}\" >\n".format(i, i))
                if i == self._afd.inicial:  # verifica se o estado a ser salvo é inicial e salva
                    if i in self._afd.finais:  # se o estado inicial também for final
                        arqObj.write("<initial/>\n<final/>\n</state>")
                    else:
                        arqObj.write("<initial/>\n</state>")
                elif i in self._afd.finais:  # verifica se o estado a ser salvo é final e salva
                    arqObj.write("<final/>\n</state>")
                else:
                    arqObj.write("</state>")

            # Salvando as transicoes
            # i = Estado atual
            # d = Proximo Estado
            # j = String lida

            for (i, j) in self._afd.transicoes.keys():
                d = self._afd.transicoes[(i, j)]
                arqObj.write(
                    "\n<transition>\n\t<from>{}</from>\n\t<to>{}</to>\n\t<read>{}</read>\n\t</transition>".format(i, d,
                                                                                                                  j))

            arqObj.write("\n\t</automaton>")
            arqObj.write("\n</structure>")
            arqObj.close()

            threading.Thread(target=abrirJFLAP, args=(self._nomeArq, )).start()

            print("\nAFD salvo com sucesso !")
        except Exception as Erro:
            print("\nErro ao salvar o arquivo ! {}".format(Erro))

def abrirJFLAP(nomeArq):
        os.system(f'cmd /k "java -jar JFLAP7.1.jar {nomeArq}.jff"')
