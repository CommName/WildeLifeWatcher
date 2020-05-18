
from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def insertImage(self, time, coordinateN, coordinateE):
        pass

    @abstractmethod
    def getImageNames(self, coordinateN, coordinateE):
        pass


