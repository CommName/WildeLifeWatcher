
from abc import ABC, abstractmethod
class Sensor(ABC):

    @abstractmethod
    def getFrame(self):
        pass