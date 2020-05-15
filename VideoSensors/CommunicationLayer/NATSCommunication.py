import asyncio
from time import sleep

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

class NATSCommunication:

    nc = None
    sid = None



    async def closeConnection(self):
        #await self.nc.unsubscribe(self.sid)
        await self.nc.close()

    async def connect(self, address=""):
        self.nc = NATS()
        await self.nc.connect()
        self.sid = await self.nc.subscribe("test", cb=self.recvMessage)

    async def sendMessage(self, msg):
        await self.nc.publish("test", b'test')
        #await nc.publish("updates", json.dumps({"symbol": "GOOG", "price": 1200 }).encode())

    async def recvMessage(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(msg)
        #await self.nc.publish(reply, b'I can help')




async def run(loop):
    test = NATSCommunication()
    await test.connect()

    for i in range(5):
        await test.sendMessage(str(i))

    await asyncio.sleep(1,loop)
    await test.closeConnection()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()