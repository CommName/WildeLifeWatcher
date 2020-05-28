
from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def insertAnalyticData(self, time, coordinateN, coordinateE):
        pass

    @abstractmethod
    def getAnalyticData(self, imageName, animals):
        pass





