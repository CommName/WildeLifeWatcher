import cherrypy
import datetime
from bson.json_util import dumps

@cherrypy.expose
class DataBaseAPI(object):

    Logic = None;

    def __init__(self, logic):
        print('construct')
        self.Logic = logic

    @cherrypy.tools.accept(media = "text/plain")
    def GET(self, coordinateN=None, coordinateE=None, startTime=None, endTime=None):

        if coordinateN == None:
            coordinateN = { "$regex": "." }

        if coordinateE == None:
            coordinateE = { "$regex": "." }

        if startTime == None:
            startTime = datetime.datetime(2020, 5, 20)

        if endTime == None:
            endTime = datetime.datetime.today()

        result =  dumps(self.Logic.storage.getImages(coordinateN,coordinateE, startTime,endTime))
        return result




    def POST(self, coordinateN, coordinateE, image):
        self.Logic.newImage(coordinateN, coordinateE, image)
