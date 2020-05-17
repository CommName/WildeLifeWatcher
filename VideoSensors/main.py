from CommunicationLayer import NATSCommunication
import cv2
import asyncio
import argparse

from Sensors import CSVSensor


class Logic:
    lastFrame = None
    coordinateN = 0
    coordinateE = 0
    frameRate = 1

    async def run(self, loop, args):
        sensor = self.getSensor(args)
        #communicator
        communciator = NATSCommunication.NATSCommunication()
        communciator.logic = self
        await communciator.connect(args["NATSaddress"])

        self.lastFrame = sensor.getFrame()
        while not (self.lastFrame is None):
            await communciator.sendMessage(self.lastFrame,self.coordinateN,self.coordinateE)
            await asyncio.sleep(1)
            self.lastFrame = sensor.getFrame()




    async def getCommunicator(self, args):
        communciator = NATSCommunication.NATSCommunication()
        communciator.logic = self
        await communciator.connect(args["NATSaddress"])
        return communciator

    def getSensor(self, args):
        sensor = CSVSensor.CSVSensor();
        sensor.loadCVSFile(args["CSVFile"])
        return sensor


#Main program
ap = argparse.ArgumentParser()
ap.add_argument("-NATS", "--NATSaddress", required=False,default="nats://localhost:4222", help="Address to NATS server")
ap.add_argument("-csv", "--CSVFile", required=True, help="CSV File with urls to images that will be displayed")
ap.add_argument("-fps", "--FramesPerSecond", required=False, default=1, help="Number of frames per second that are sendt throught network")
ap.add_argument("-N", "--NorthCoordiante", required=True, help="Noorth gps coordinate of sensor")
ap.add_argument("-E", "--EastCoordinate", required=True, help="East gps coordinate of sensor")
args = vars(ap.parse_args())

logic = Logic()

logic.coordinateE = args["EastCoordinate"]
logic.coordinateN = args["NorthCoordiante"]
logic.frameRate = args["FramesPerSecond"]

loop = asyncio.get_event_loop()
loop.run_until_complete(logic.run(loop, args))
loop.close()