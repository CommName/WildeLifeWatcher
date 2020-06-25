import cherrypy
import datetime
import json
import os

@cherrypy.expose
class ImageAPI(object):

    Logic = None;

    def __init__(self, logic):
        self.Logic = logic


    def GET(self, imageName):
        results = self.Logic.storage.getAnalyticData(imageName)
        if results is not None:
            del results["_id"]
        return json.dumps(results).encode()

    def POST(self, imageName, image):
        self.Logic.newImage(image,imageName)