import cv2
from StorageSystem import MongoStorage
from datetime import datetime
import asyncio
import os.path
from pathlib import Path
from CommunicationLayer import NATSCommunication
from API import DataBaseAPI
from API import ImageAPI

import cherrypy
import threading

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
        URI = "./images/"
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


def asyncoThreading(loop, logic):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(logic.run(loop))

#Main
logic = DataServiceLogic()

loop = asyncio.get_event_loop()
sensorThread = threading.Thread(target=asyncoThreading, args=(loop,logic,))
sensorThread.start()

dbGateway = DataBaseAPI.DataBaseAPI(logic)
imgGateway = ImageAPI.ImageAPI(logic)
conf = {
    '/': {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on' : True,
        'tools.response_headers.headers' : [('Content-Type', 'text/plain')],
    }
}

cherrypy.tree.mount(dbGateway, "/data", conf)
cherrypy.tree.mount(imgGateway, "/image", conf)

if hasattr(cherrypy.engine, 'block'):
    # 3.1 syntax
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    # 3.0 syntax
    cherrypy.server.quickstart()
    cherrypy.engine.start()