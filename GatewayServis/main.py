import time
time.sleep(3)
import cherrypy
import os
from API import WebDashboard
from API import ImageAPI
from API import MyWebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from CommunicationLayer import comm
import argparse
import asyncio
import threading
from API import SensorAPI
from API import GalleryAPI
from CommunicationLayer import ServiceRegistry

async def communicatorLayer(args):
    communicator = await comm.getCommunciator(args, None)
    while True:
        await asyncio.sleep(1000)

def communicationThread(loop, args):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(communicatorLayer(args))


#TODO Drugacije implementirati ovaj deo


ag = argparse.ArgumentParser()
ag.add_argument('-c', '--communicator',required=False, default="NATS", help="Type of communciator to be used")
ag.add_argument('-ns', "--NATSaddress", required=False, default="nats://localhost:4222", help="Address of NATS server")
ag.add_argument('-r', "--serviceRegistryAddress", required=False, default="http://127.0.0.1:8761/", help="Service registry address")
ag.add_argument('-p', "--port", required=False, default="8080", help="Port of the service")
ag.add_argument('-n', "--name", required=False, default="Gateway", help="Name of the sensor")
ag.add_argument('-d', "--domain", required=False, default="127.0.0.1:8080", help="Domain of web application")
args = vars(ag.parse_args())

if __name__ == "__main__":
    ServiceRegistry.registry("Gateway", args["name"], port=args["port"],
                             serviceRegistryAddress=args['serviceRegistryAddress'])
    #Communciator start
    communicationLoop = asyncio.get_event_loop()
    commThread = threading.Thread(target=communicationThread, args=(communicationLoop,args))
    commThread.start()

    #Cherry configuration
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'tools.sessions.on': True,
                            'tools.sessions.storage_type': "File",
                            'tools.sessions.storage_path': os.path.abspath(os.path.join(os.path.dirname( __file__ ), "sessions")),
                            'tools.sessions.timeout': 10
                            })

    #Cherrypy API config
    web_conf = {
        '/': {
            'tools.sessions.on' : True,
            'tools.response_headers.on': True,
            'tools.staticdir.root' : os.path.abspath(os.path.join(os.path.dirname( __file__ ))),
            'tools.response_headers.headers': [
                ('X-Frame-options', 'deny'),
                ('X-XSS-Protection', '1; mode=block'),
                ('X-Content-Type-Options', 'nosniff')
                ]
        },

        '/style.css': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.abspath(os.path.join(os.path.dirname( __file__ ))) + '/Public/CSS/style.css'
        },
        '/notifications.css': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.abspath(os.path.join(os.path.dirname( __file__ ))) + '/Public/CSS/notifications.css'
        },

        '/scripts': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './Public/JS/'
        },

        '/ws' : {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': MyWebSocket.WebSocketHandler
        }
    }

    sensor_conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        }
    }



    #Creating API objects
    web = WebDashboard.WebDashboard(args["domain"])
    imgAPI = ImageAPI.ImageAPI()
    sensorAPI = SensorAPI.SensorAPI()
    galleryAPI = GalleryAPI.GalleryAPI()

    #Mounting objects
    cherrypy.tree.mount(web, '/', web_conf)
    cherrypy.tree.mount(imgAPI,'/images')
    cherrypy.tree.mount(sensorAPI, '/sensors', sensor_conf)
    cherrypy.tree.mount(galleryAPI,'/galleryData')

    #Starting
    cherrypy.engine.start()
    cherrypy.engine.block()