import cherrypy
import datetime
from bson.json_util import dumps
import os

@cherrypy.expose
class ImageAPI(object):

    Logic = None;

    def __init__(self, logic):
        self.Logic = logic


    def GET(self, imageName = { "$regex": "." }, animalName = None):
        print("test")
        return dumps(self.Logic.storage.getAnalyticData(imageName, animalName))

    def POST(self, imageName, image):
        self.Logic.newImage(image,imageName)