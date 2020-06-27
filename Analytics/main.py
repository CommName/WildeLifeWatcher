import argparse
import asyncio
import cherrypy
import threading
from CommunicationLayer import comm
from StorageSystem import stor
from DataAnalyser import analy
from API import DBapi
import requests
from CommunicationLayer import ServiceRegistry
from API import ImageInformationApi

class Logic:

    storage = None
    communicator = None



    async def newImage(self, image, imageName, coordinateN, coordinateE):
        #analyse image
        analysedData = self.analyser.analyseImage(image)
        print(analysedData)
        if(analysedData==None):
            return


        
        analysedData["imageName"] = imageName
        #save results
        self.storage.insertAnalyticData(analysedData)

        #notify others
        await self.communicator.sendMessage(analysedData)

        if "Eating" not in analysedData or analysedData["Eating"]==False:
            serviceList = ServiceRegistry.getServices("Command")
            parametars = {
                "coordinateN" : coordinateN,
                "coordinateE" : coordinateE,
                "listOfParamtears" : "Give food"
            }

            for service in serviceList:
                try:
                    r = requests.post(service["ServiceAddress"]+"/command", params=parametars)
                    return
                except requests.exceptions.RequestException:
                    continue


    async def run(self, loop, args):
        self.storage = stor.getStorage(args)
        print("[INFO] Storage initialze")
        self.analyser = analy.getAnalyser(args)
        print("[INFO] Analyser initialze")
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
ap.add_argument('-p', '--port', default="9020", required=False, help='Port on which API runs')
ap.add_argument('-a', '--analyser', default="VGG16", required=False, help='Analyzing algorthm used')
ap.add_argument('-n', '--name', default="VGG16Analytics", required=False, help='Name of service')
ap.add_argument('-em', '--EatingModel', default="EatingModel.model", required=False, help='Name of service')
ap.add_argument('-r', "--serviceRegistryAddress", required=False, default="http://127.0.0.1:8761/", help="Service registry address")



args = vars(ap.parse_args())
args["port"] = int(args["port"])


#connection loop
logic = Logic()
loop = asyncio.get_event_loop()
sensorThread = threading.Thread(target=asyncoThreading, args=(loop,logic,args,))
sensorThread.start()

#Consul
ServiceRegistry.registry("Analytics",args["name"], port= args["port"],serviceRegistryAddress=args['serviceRegistryAddress'])

#chery pie api
dbGateway = DBapi.ImageAPI(logic)
informationGateway = ImageInformationApi.InfomrationSearchAPI(logic)

cherrypy.config.update({'server.socket_port': args["port"],
                        'server.socket_host': '0.0.0.0'
                        })

conf = {
    '/': {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on' : True,
        'tools.response_headers.headers' : [('Content-Type', 'text/plain')],
    }
}

cherrypy.tree.mount(dbGateway, "/imageSearch", conf)
cherrypy.tree.mount(informationGateway, "/informationSearch", conf)

if hasattr(cherrypy.engine, 'block'):
    # 3.1 syntax
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    # 3.0 syntax
    cherrypy.server.quickstart()
    cherrypy.engine.start()

