import argparse
import asyncio
import cherrypy
import threading
from CommunicationLayer import comm
from StorageSystem import stor
from DataAnalyser import analy
from API import DBapi
import consul
from consul import Check
from dns import resolver

class Logic:

    storage = None
    communicator = None
    analyser = None


    async def newImage(self, image, imageName):
        #analyse image
        analysedData = self.analyser.analyseImage(image)

        if(analysedData==None):
            return

        #save results
        self.storage.insertAnalyticData(imageName,analysedData)

        #notify others
        self.communicator.sendMessage(imageName,analysedData)


    async def run(self, loop, args):
        self.analyser = analy.getAnalyser(args)
        print("[INFO] Analyser initialze")
        self.storage = stor.getStorage(args)
        print("[INFO] Storage initialze")
        self.communicator = await comm.getCommunciator(args,self)
        print("[INFO] Communicator initialze")

        while True:
            await asyncio.sleep(1)


def asyncoThreading(loop, logic, args):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(logic.run(loop, args))






#Main
#arguments
ap = argparse.ArgumentParser()
ap.add_argument('-d', '--DataBaseAddress', default="mongodb://localhost:27017", required=False, help='Address to DataBase server')
ap.add_argument('-ns', '--NATSaddress', default="nats://localhost:4222", required=False, help='Address to NATS server')
ap.add_argument('-db', '--DataBase', default="Mongo", required=False, help='Type of DataBase to be used')
ap.add_argument('-c', '--communicator', default="NATS", required=False, help='Type of Communciator to be used')
ap.add_argument('-p', '--port', default="9000", required=False, help='Port on which API runs')
ap.add_argument('-a', '--analyser', default="VGG16", required=False, help='Analyzing algorthm used')
args = vars(ap.parse_args())
args["port"] = int(args["port"])


#connection loop
logic = Logic()
loop = asyncio.get_event_loop()
sensorThread = threading.Thread(target=asyncoThreading, args=(loop,logic,args,))
sensorThread.start()

#Consul

#chery pie api
dbGateway = DBapi.ImageAPI(logic)

cherrypy.config.update({'server.socket_port': args["port"]})

conf = {
    '/': {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on' : True,
        'tools.response_headers.headers' : [('Content-Type', 'text/plain')],
    }
}

cherrypy.tree.mount(dbGateway, "/", conf)

if hasattr(cherrypy.engine, 'block'):
    # 3.1 syntax
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    # 3.0 syntax
    cherrypy.server.quickstart()
    cherrypy.engine.start()



c.agent.service.deregister("analytics")