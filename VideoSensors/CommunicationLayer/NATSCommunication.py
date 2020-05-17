import asyncio
import json
from nats.aio.client import Client as NATS
import cv2
from CommunicationLayer import Communicator

class NATSCommunication (Communicator):

    nc = None
    sid = None
    sendTopicName = "WildLife.Sensors.Data"
    recvTopicRequest = "WildLife.Sensors.API"
    logic = None

    async def addHandler(self, obj, command, arguments):
        return obj

    async def closeConnection(self):
        await self.nc.close()

    async def connect(self, address="nats://localhost:4222"):
        self.nc = NATS()
        await self.nc.connect(address)
        self.sid = await self.nc.subscribe(self.recvTopicRequest, cb=self.recvMessage)

    async def sendMessage(self, image, gpsNCoordinate, gpsYCoordinate):
        jsonData = super().encodeMessageJSON()
        await self.nc.publish(self.sendTopicName, jsonData.encode())


    async def recvMessage(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = json.loads(msg.data.decode())
        
        #await self.nc.publish(reply, b'I can help')



