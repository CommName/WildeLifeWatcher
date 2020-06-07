import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket
import os

class WebDashboard:
    indexPage = None
    liveStreamPage = None

    ws_addr = None

    def __init__(self, address="127.0.0.1:8080"):
        self.ws_addr =  address

        cur_dir = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
        index_path = "./Public/HTML/index.html"
        self.indexPage = open(index_path, 'r').read()
        liveStream_path = "./Public/HTML/LiveStream.html"
        self.liveStreamPage = open(liveStream_path, 'r').read()


    @cherrypy.expose
    def index(self):
        return self.indexPage

    @cherrypy.expose
    def Home(self):
        return self.index()

    @cherrypy.expose
    def Live(self):
        return self.liveStreamPage % {'ws_addr': self.ws_addr}

    @cherrypy.expose
    def Gallery(self):
        return self.indexPage % {'username': "User123" , 'ws_addr': self.ws_addr}

    @cherrypy.expose
    def ws(self):
        handler = cherrypy.request.ws_handler