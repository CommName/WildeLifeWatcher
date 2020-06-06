
from abc import ABC, abstractmethod


class Communicator(ABC):



    @abstractmethod
    async def sendMessage(self, msg):
        pass



