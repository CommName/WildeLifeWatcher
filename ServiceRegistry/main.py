from time import sleep
import argparse
from RegistryFiles import Registry
import threading
import asyncio
from CommunicationLayer import comm
from API import ServiceRegistryAPI
import cherrypy

async def communicatorLayer(args):
    communicator = await comm.getCommunciator(args)
    Registry.Registry.Instance().communicator = communicator
    while True:
        await asyncio.sleep(1000)

def communicationThread(loop, args):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(communicatorLayer(args))


ag = argparse.ArgumentParser()
ag.add_argument('-c', '--communicator',required=False, default="NATS", help="Type of communciator to be used")
ag.add_argument('-ns', "--NATSaddress", required=False, default="nats://localhost:4222", help="Address of NATS server")
ag.add_argument('-p', "--port", required=False, default="8761", help="Port of the service")
args = vars(ag.parse_args())
args["port"] = int(args["port"])


Registry.Registry.Instance()

if __name__ == "__main__":

    #Communciator start
    communicationLoop = asyncio.get_event_loop()
    commThread = threading.Thread(target=communicationThread, args=(communicationLoop,args))
    commThread.start()

    #Cherrpy
    cherrypy.config.update({'server.socket_port': args["port"]})
    cherrypy.config.update({'server.socket_host':'0.0.0.0'})

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        }
    }

    api = ServiceRegistryAPI.ServiceRegistryAPI()
    cherrypy.tree.mount(api,'/',conf )
    cherrypy.engine.start()
    cherrypy.engine.block()