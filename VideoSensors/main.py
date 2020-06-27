from CommunicationLayer import NATSCommunication
from CommunicationLayer import ServiceRegistry
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
    Name = ""
    frameRate = 1
    args = None
    sensor = None
    communciator = None

    def __init__(self, args):

        self.args = args
        self.coordinateE = float(args["EastCoordinate"])
        self.coordinateN = float(args["NorthCoordiante"])
        self.frameRate = int(args["FramesPerSecond"])
        self.Name = args["name"]

    async def run(self, loop):
        self.sensor = self.getSensor()
        #communicator
        self.communciator = NATSCommunication.NATSCommunication()
        self.communciator.logic = self
        await self.communciator.connect(args["NATSaddress"])

        self.sensor.skipFrames((args["skipFirstNFrames"]))

        self.lastFrame = self.sensor.getFrame()
        index = 0

        while not (self.lastFrame is None):
            await self.communciator.sendMessage(self.lastFrame,self.coordinateN,self.coordinateE,self.Name)
            print("Image number "+str(index)+" has been sent!")
            index +=1
            await asyncio.sleep(1//self.frameRate)
            self.lastFrame = self.sensor.getFrame()


    async def getCommunicator(self):
        communciator = NATSCommunication.NATSCommunication()
        communciator.logic = self
        await communciator.connect(args["NATSaddress"])
        return communciator

    def getSensor(self):
        sensor = CSVSensor.CSVSensor();
        sensor.loadCVSFile(args["CSVFile"])
        return sensor


def asyncoThreading(loop, logic):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(logic.run(loop))

ag = argparse.ArgumentParser()
ag.add_argument('-p', "--port", required=False, default="9000", help="Port of the service")
ag.add_argument('-n', "--name", required=False, default="First sensor", help="Name of the sensor")
ag.add_argument('-ns', "--NATSaddress", required=False, default="nats://localhost:4222", help="Address of NATS server")
ag.add_argument('-csv', "--CSVFile", required=False, default="dataset.csv", help="Name of csv file to be used as data")
ag.add_argument('-N', "--NorthCoordiante", required=False, default="40.0", help="North Coordinate of sensor")
ag.add_argument('-E', "--EastCoordinate", required=False, default="40.0", help="East coordinate of sensor")
ag.add_argument('-fps', "--FramesPerSecond", required=False, default="1", help="Frames per second")
ag.add_argument('-r', "--serviceRegistryAddress", required=False, default="http://127.0.0.1:8761/", help="Service registry address")
ag.add_argument('-s', "--skipFirstNFrames", required=False, default="0", help="Skip first N data")


args = vars(ag.parse_args())
args["port"] = int(args["port"])
args["FramesPerSecond"] = int(args["FramesPerSecond"])
args["NorthCoordiante"] = float(args["NorthCoordiante"])
args["EastCoordinate"] = float(args["EastCoordinate"])
args["skipFirstNFrames"] = int(args["skipFirstNFrames"])

#Main program
logic = Logic(args)




loop = asyncio.get_event_loop()
sensorThread = threading.Thread(target=asyncoThreading, args=(loop,logic,))
sensorThread.start()

ServiceRegistry.registry("Sensors",args["name"], port= args["port"],serviceRegistryAddress=args['serviceRegistryAddress'])

API = APIGateway.Gateway(logic)
cherrypy.config.update({'server.socket_port': args["port"]})
cherrypy.config.update({'server.socket_host': '0.0.0.0'})

conf = {
    '/': {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on' : True,
        'tools.response_headers.headers' : [('Content-Type', 'text/plain')],
    }
}

cherrypy.quickstart(API,'/',conf)


