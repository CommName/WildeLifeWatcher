
from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def insertAnalyticData(self, analyticData):
        pass

    @abstractmethod
    def getAnalyticData(self, imageName):
        pass





