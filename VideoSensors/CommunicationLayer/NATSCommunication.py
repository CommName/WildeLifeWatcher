import asyncio
import json
from nats.aio.client import Client as NATS
import cv2
from CommunicationLayer import Communicator

class NATSCommunication (Communicator.Communicator):
    nc = None
    sid = None
    sendTopicName = "WildLife.Sensors.Data"
    logic = None



    async def closeConnection(self):
        await self.nc.close()

    async def connect(self, address="nats://localhost:4222"):
        self.nc = NATS()
        await self.nc.connect(address)

    async def sendMessage(self, image, gpsNCoordinate, gpsYCoordinate, Name):
        jsonData = super().encodeMessageJSON(image, gpsNCoordinate, gpsYCoordinate, Name)
        await self.nc.publish(self.sendTopicName, jsonData.encode())






