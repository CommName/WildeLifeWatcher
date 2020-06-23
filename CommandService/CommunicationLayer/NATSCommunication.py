import asyncio
import json
from nats.aio.client import Client as NATS
import cv2
from CommunicationLayer import Communicator

class NATSCommunication (Communicator.Communicator):
    nc = None
    sid = None
    analyticsTopicName = "WildLife.Analytics"
    dataTopicName = "WildLife.Information"
    logic = None



    async def closeConnection(self):
        await self.nc.close()

    async def connect(self, address="nats://localhost:4222"):
        self.nc = NATS()
        await self.nc.connect(address)
        await self.nc.subscribe(self.analyticsTopicName, cb= self.recvMessage)

    async def sendMessage(self, analysticData):
        del analysticData['_id']
        jsonData = json.dumps(analysticData)
        await self.nc.publish(self.dataTopicName, jsonData.encode())
        print(jsonData)

    async def recvMessage(self, msg):
        print(msg)
        subject = msg.subject
        reply = msg.reply
        data = json.loads(msg.data.decode())
        image,imageName = super().decodeMessageJSON(data)
        await self.logic.newImage(image,imageName)




