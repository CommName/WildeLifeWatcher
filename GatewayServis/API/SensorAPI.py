import cherrypy
import requests
from NotificationRegistry import NotificationRegistry
import json

@cherrypy.expose
class SensorAPI(object):

    address = "http://127.0.0.1:8761/"


    def GET(self):
        return json.dumps(NotificationRegistry.NotificationRegistry.Instance().serviceRegistry.getUserSensors())


