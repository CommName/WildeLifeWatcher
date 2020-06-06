from nats.aio.client import Client as NATS
from CommunicationLayer import Communicator

class NATSCommunication (Communicator.Communicator):

    nc = None
    notifyTopic = "WildLife.Registry"

    async def closeConnection(self):
        await self.nc.close()

    async def connect(self, address="nats://localhost:4222"):
        self.nc = NATS()
        print(address)
        await self.nc.connect(address)

    async def sendMessage(self, msg):
        await self.nc.publish(self.notifyTopic, msg.encode('ascii'))
        return
