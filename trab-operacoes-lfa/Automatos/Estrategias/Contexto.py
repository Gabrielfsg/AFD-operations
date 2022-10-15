from .Estrategia import Estrategia

class Contexto:

    def __init__(self,estrategia: Estrategia = None):
        self._estrategia = estrategia

    #Get pro objeto
    @property
    def estrategia(self):
        return self._estrategia

    @estrategia.setter
    def estrategia(self,estrategia: Estrategia):
        self._estrategia = estrategia

    #Posso enviar argumentos opcionais pro método (útil em estratégias de leitura/escrita de um Automato)
    def executarOperacao(self):
        return self._estrategia.operacao()
