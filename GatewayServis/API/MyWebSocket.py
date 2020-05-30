import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

class WebSocketHandler(WebSocket):
    def opened(self):
        self.send(TextMessage('Welcome'))

    def received_message(self, m):
        cherrypy.engine.publish('websocket-broadcast', m)
        self.send(TextMessage("pong"), False)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))