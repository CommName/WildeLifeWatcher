import cherrypy
import json


@cherrypy.expose
class ImageInfo(object):

    Logic = None;

    def __init__(self, logic):
        self.Logic = logic


    def GET(self, imageName):
        result  = self.Logic.storage.getImageDetials(imageName)
        result["id"] = str(result["_id"])
        del result["_id"]

        result["time"] = str(result["time"])
        return json.dumps(result).encode()