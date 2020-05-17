from CommunicationLayer import NATSCommunication
import asyncio
import argparse
import os

from Sensors import CSVSensor


class Logic:
    lastFrame = None
    coordinateN = 0
    coordinateE = 0
    frameRate = 1

    async def run(self, loop):
        sensor = self.getSensor()
        #communicator
        communciator = NATSCommunication.NATSCommunication()
        communciator.logic = self
        await communciator.connect(os.getenv("NATSaddress"))

        self.lastFrame = sensor.getFrame()
        while not (self.lastFrame is None):
            await communciator.sendMessage(self.lastFrame,self.coordinateN,self.coordinateE)

            await asyncio.sleep(1//self.frameRate)
            self.lastFrame = sensor.getFrame()




    async def getCommunicator(self):
        communciator = NATSCommunication.NATSCommunication()
        communciator.logic = self
        await communciator.connect(os.getenv("NATSaddress"))
        return communciator

    def getSensor(self):
        sensor = CSVSensor.CSVSensor();
        sensor.loadCVSFile(os.getenv("CSVFile"))
        return sensor


#Main program
logic = Logic()
print(os.environ)
logic.coordinateE = float(os.getenv("EastCoordinate"))
logic.coordinateN = float(os.getenv("NorthCoordiante"))
logic.frameRate = int(os.getenv("FramesPerSecond"))

loop = asyncio.get_event_loop()
loop.run_until_complete(logic.run(loop))
loop.close()