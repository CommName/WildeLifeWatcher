import cherrypy
import datetime
from bson.json_util import dumps
import os

@cherrypy.expose
class ImageAPI(object):

    Logic = None;

    def __init__(self, logic):
        print('construct')
        self.Logic = logic

    @cherrypy.tools.accept(media = "text/plain")
    def GET(self, imageName = ""):

        if(imageName!=""):
            url = "./images/"+imageName+".jpg"
            if os.path.isfile(url):
                image = open(url, 'rb')
                data = image.read()
                cherrypy.response.headers["Content-Type"] = 'image/jpeg'
                return data

        return

