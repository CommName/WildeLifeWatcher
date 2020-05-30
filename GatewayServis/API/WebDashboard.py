import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket
import os

class WebDashboard:
    indexPage = None

    def __init__(self):
        cur_dir = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
        index_path = "./Public/index.html"
        self.indexPage = open(index_path, 'r').read()


    @cherrypy.expose
    def index(self):
        return self.indexPage % {'username': "User123" , 'ws_addr': 'ws://localhost:8080/ws'}

    @cherrypy.expose
    def ws(self):
        handler = cherrypy.request.ws_handler