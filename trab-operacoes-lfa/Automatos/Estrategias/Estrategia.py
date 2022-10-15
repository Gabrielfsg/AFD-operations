from abc import ABC, abstractmethod

class Estrategia(ABC):

    @abstractmethod
    def operacao(self):
        pass
