import asyncio
import json
from nats.aio.client import Client as NATS
import cv2
from CommunicationLayer import Communicator

class NATSCommunication (Communicator.Communicator):
    nc = None
    sid = None
    sensorsTopicName = "WildLife.Sensors.Data"
    analyticsTopicName = "WildLife.Analytics"
    requestTopicName = "WildLife.Data"
    logic = None



    async def closeConnection(self):
        await self.nc.close()

    async def connect(self, address="nats://localhost:4222"):
        self.nc = NATS()
        await self.nc.connect(address)

        await self.nc.subscribe(self.sensorsTopicName, cb= self.recvMessageFromSensors)
        await self.nc.subscribe(self.requestTopicName, cb= self.recvRequest)
        print(address)
        print(self.sensorsTopicName)

    async def sendMessage(self, image, imageId):
        jsonData = super().encodeMessageJSON(image,imageId)
        await self.nc.publish(self.analyticsTopicName, jsonData.encode())

    async def recvRequest(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = json.loads(msg.data.decode())


    async def recvMessageFromSensors(self, msg):
        print(msg)
        subject = msg.subject
        reply = msg.reply
        data = json.loads(msg.data.decode())
        image, N, E = super().decodeMessageJSON(data)
        await self.logic.newImage(image,N,E)




