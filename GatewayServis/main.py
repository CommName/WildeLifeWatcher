import cherrypy
import os
from API import WebDashboard
from API import ImageAPI
from API import MyWebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket
from NotificationRegistry import NotificationRegistry
from CommunicationLayer import comm
import argparse
import asyncio
import threading

async def communicatorLayer(args):
    communicator = await comm.getCommunciator(args, None)
    while True:
        await asyncio.sleep(1000)

def communicationThread(loop, args):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(communicatorLayer(args))


#TODO Drugacije implementirati ovaj deo
NotificationRegistry.NotificationRegistry.Instance().addSensor(40.0,40.0)


ag = argparse.ArgumentParser()
ag.add_argument('-c', '--communicator',required=False, default="NATS", help="Type of communciator to be used")
ag.add_argument('-ns', "--NATSaddress", required=False, default="nats://localhost:4222", help="Address of NATS server")
args = vars(ag.parse_args())

if __name__ == "__main__":

    #Communciator start
    communicationLoop = asyncio.get_event_loop()
    commThread = threading.Thread(target=communicationThread, args=(communicationLoop,args))
    commThread.start()

    #Cherry configuration
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    #Cherrypy API config
    web_conf = {
        '/': {
            'tools.sessions.on' : True,
            'tools.response_headers.on': True,
            'tools.staticdir.root' : os.path.abspath(os.getcwd()),
            'tools.response_headers.headers': [
                ('X-Frame-options', 'deny'),
                ('X-XSS-Protection', '1; mode=block'),
                ('X-Content-Type-Options', 'nosniff')
                ]
        },

        '/style.css': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.abspath(os.getcwd()) + '/Public/CSS/style.css'
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



    #Creating API objects
    web = WebDashboard.WebDashboard()
    imgAPI = ImageAPI.ImageAPI()

    #Mounting objects
    cherrypy.tree.mount(web, '/', web_conf)
    cherrypy.tree.mount(imgAPI,'/images')

    #Starting
    cherrypy.engine.start()
    cherrypy.engine.block()