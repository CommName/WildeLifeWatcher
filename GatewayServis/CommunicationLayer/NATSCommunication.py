import asyncio
import json
from nats.aio.client import Client as NATS
import cv2
from CommunicationLayer import Communicator
from NotificationRegistry import NotificationRegistry

class NATSCommunication (Communicator.Communicator):
    nc = None
    sid = None
    sensorsTopicName = "WildLife.Sensors.Data"
    logic = None
    registryTopic = "WildLife.Registry"



    async def closeConnection(self):
        await self.nc.close()


    async def connect(self, address="nats://localhost:4222"):
        self.nc = NATS()
        await self.nc.connect(address)
        await self.nc.subscribe(self.registryTopic,cb=self.registryChange)
        await self.nc.subscribe(self.sensorsTopicName, cb= self.recvMessageFromSensors)


    async def registryChange(self, msg):
        print(msg.data)
        NotificationRegistry.NotificationRegistry.Instance().serviceRegistry.reloadSensors()


    async def recvMessageFromSensors(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = json.loads(msg.data.decode())
        image, N, E, sensorName = super().decodeMessageJSON(data)
        print("New image from "+sensorName)
        NotificationRegistry.NotificationRegistry.Instance().notifySensor(image,sensorName)