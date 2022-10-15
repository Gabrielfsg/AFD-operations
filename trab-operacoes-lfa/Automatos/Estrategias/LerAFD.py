import xml.etree.ElementTree as ET
from .Estrategia import Estrategia
from ..AutomatoFD import AutomatoFD
import traceback

class LerAFD(Estrategia):

    def __init__(self,dir):
        self._dir = dir

    def operacao(self) -> AutomatoFD:

        try:
            alfabeto = ''
            Estado = 1
            arq = open(self._dir, "r")
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

            # Cria o automato a partir do alfabeto obtido
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

        except Exception:
            print(traceback.format_exc())