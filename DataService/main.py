import cv2
from StorageSystem import MongoStorage
from datetime import datetime
import asyncio
from pathlib import Path
from CommunicationLayer import NATSCommunication
from API import DataBaseAPI
from API import ImageAPI
from CommunicationLayer import ServiceRegistry
import cherrypy
import threading
import argparse
from CommunicationLayer import comm
from StorageSystem import comm as commDb
from API import ImageInfo

class DataServiceLogic:

    storage = None
    communicator = None
    args = None

    def __init__(self, args):
        self.args = args




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
        await self.communicator.sendMessage(image, imageId, coordinateN, coordinateE)

    async def run(self, loop):
        self.storage = commDb.getDatabase(self.args)
        self.communicator = await comm.getCommunciator(self.args, self)

        while True:
            await asyncio.sleep(1)


def asyncoThreading(loop, logic):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(logic.run(loop))

#Main
ag = argparse.ArgumentParser()
ag.add_argument('-p', "--port", required=False, default="9010", help="Port of the service")
ag.add_argument('-n', "--name", required=False, default="Data1", help="Name of the sensor")
ag.add_argument('-c', '--communicator',required=False, default="NATS", help="Type of communciator to be used")
ag.add_argument('-ns', "--NATSaddress", required=False, default="nats://localhost:4222", help="Address of NATS server")
ag.add_argument('-db', "--DataBase", required=False, default="Mongo", help="Type of DB to use")
ag.add_argument('-DBa', "--DataBaseAddress", required=False, default="mongodb://localhost:27017", help="Address of Mongo database")
ag.add_argument('-r', "--serviceRegistryAddress", required=False, default="http://127.0.0.1:8761/", help="Service registry address")


args = vars(ag.parse_args())
args["port"] = int(args["port"])

logic = DataServiceLogic(args)

ServiceRegistry.registry("Data",args["name"], port= args["port"],serviceRegistryAddress=args['serviceRegistryAddress'])

loop = asyncio.get_event_loop()
sensorThread = threading.Thread(target=asyncoThreading, args=(loop,logic,))
sensorThread.start()


cherrypy.config.update({'server.socket_port': args["port"]})
cherrypy.config.update({'server.socket_host': '0.0.0.0'})

dbGateway = DataBaseAPI.DataBaseAPI(logic)
imgGateway = ImageAPI.ImageAPI(logic)
imgInfoGateway = ImageInfo.ImageInfo(logic)

conf = {
    '/': {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on' : True,
        'tools.response_headers.headers' : [('Content-Type', 'text/plain')],
    }
}

cherrypy.tree.mount(dbGateway, "/data", conf)
cherrypy.tree.mount(imgGateway, "/image", conf)
cherrypy.tree.mount(imgInfoGateway, "/info", conf)


if hasattr(cherrypy.engine, 'block'):
    # 3.1 syntax
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    # 3.0 syntax
    cherrypy.server.quickstart()
    cherrypy.engine.start()