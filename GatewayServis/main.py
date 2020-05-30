import cherrypy
import os
from API import WebDashboard
from API import ImageAPI
from API import MyWebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket




if __name__ == "__main__":

    #Cherry configuration
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    #Cherrypy API config
    web_conf = {
        '/': {
            'tools.sessions.on' : True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [
                ('X-Frame-options', 'deny'),
                ('X-XSS-Protection', '1; mode=block'),
                ('X-Content-Type-Options', 'nosniff')
                ]
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