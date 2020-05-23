
from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def insertImage(self, time, coordinateN, coordinateE):
        pass

    @abstractmethod
    def getImageNames(self, coordinateN, coordinateE):
        pass

    def getImages(self, coordinateN, coordinateE, startTime, endTime):
        pass


