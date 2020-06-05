import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from NotificationRegistry import NotificationRegistry

class WebSocketHandler(WebSocket):

    subscribedSensors = []


    def opened(self):
        NotificationRegistry.NotificationRegistry.Instance().subscribeForSensor(40.0, 40.0,self)

    def received_message(self, m):
        #TODO subscribe for diffrent things

        #sensor N E

        #unsub sensor N E

        #animal animalName

        #unsub animal animalName

        return


    def closed(self):
        for sensor in self.subscribedSensors:
            sensor.unsubsribe(self)

    def unsubcribeSensor(self, senosr):
        self.subscribedSensors.remove(senosr)

    def subscribeSensor(self, sensor):
        self.subscribedSensors.append(sensor)