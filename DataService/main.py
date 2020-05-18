import asyncio
from nats.aio.client import Client as NATS
import cv2
import json
import base64
import numpy as np
from StorageSystem import MongoStorage
from datetime import datetime
import asyncio
import os.path
from pathlib import Path
from CommunicationLayer import NATSCommunication


class DataServiceLogic:

    storage = None
    communicator = None


    async def getCommunicator(self):
        communicator = NATSCommunication.NATSCommunication()
        communicator.logic = self
        await communicator.connect(os.getenv('NATSaddress'))
        return communicator

    def getStorage(self):
        mongo = MongoStorage.MongoStorage(os.getenv("DBaddress"))
        return mongo

    async def newImage(self, image, coordinateN, coordinateE):
        time = datetime.now()

        #Save image atributes
        imageId = self.storage.insertImage(time,coordinateN, coordinateE)

        #Save iamge
        URI = "./images/"+str(coordinateN)+"/"+str(coordinateE)+"/"
        filepath = Path(URI)
        filepath.mkdir(parents=True,exist_ok=True)
        URI += str(imageId)+".jpg"
        cv2.imwrite(URI,image)

        #Broadcast to the rest
        await self.communicator.sendMessage(image, imageId)

    async def run(self, loop):
        self.storage = self.getStorage()
        self.communicator = NATSCommunication.NATSCommunication()
        self.communicator.logic = self
        await self.communicator.connect(os.getenv('NATSaddress'))

        while True:
            await asyncio.sleep(1)




logic = DataServiceLogic()

loop = asyncio.get_event_loop()
loop.run_until_complete(logic.run(loop))
loop.close()



