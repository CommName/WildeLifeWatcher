from CommunicationLayer import NATSCommunication
import asyncio
import argparse
import os
import APIGateway
import cherrypy
import threading

from Sensors import CSVSensor

class Logic:
    lastFrame = None
    coordinateN = 0
    coordinateE = 0
    frameRate = 1
    sensor = None
    communciator = None


    async def run(self, loop):
        self.sensor = self.getSensor()
        #communicator
        self.communciator = NATSCommunication.NATSCommunication()
        self.communciator.logic = self
        await self.communciator.connect(os.getenv("NATSaddress"))

        self.lastFrame = self.sensor.getFrame()
        while not (self.lastFrame is None):
            await self.communciator.sendMessage(self.lastFrame,self.coordinateN,self.coordinateE)

            await asyncio.sleep(1//self.frameRate)
            self.lastFrame = self.sensor.getFrame()

    async def getCommunicator(self):
        communciator = NATSCommunication.NATSCommunication()
        communciator.logic = self
        await communciator.connect(os.getenv("NATSaddress"))
        return communciator

    def getSensor(self):
        sensor = CSVSensor.CSVSensor();
        sensor.loadCVSFile(os.getenv("CSVFile"))
        return sensor


def asyncoThreading(loop, logic):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(logic.run(loop))

#Main program
logic = Logic()
print(os.environ)
logic.coordinateE = float(os.getenv("EastCoordinate"))
logic.coordinateN = float(os.getenv("NorthCoordiante"))
logic.frameRate = int(os.getenv("FramesPerSecond"))

loop = asyncio.get_event_loop()
sensorThread = threading.Thread(target=asyncoThreading, args=(loop,logic,))
sensorThread.start()

API = APIGateway.Gateway(logic)
conf = {
    '/': {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on' : True,
        'tools.response_headers.headers' : [('Content-Type', 'text/plain')],
    }
}


cherrypy.quickstart(API,'/',conf)


