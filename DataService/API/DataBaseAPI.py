import cherrypy
import datetime
from bson.json_util import dumps
import json

@cherrypy.expose
class DataBaseAPI(object):

    Logic = None;

    def __init__(self, logic):
        self.Logic = logic



    @cherrypy.tools.accept(media = "text/plain")
    def GET(self, coordinateN=None, coordinateE=None, startTime=None, endTime=None):

        if not coordinateN is None:
            coordinateN = float(coordinateN)

        if not coordinateE is None:
            coordinateE = float(coordinateE)

        if startTime == None:
            startTime = datetime.datetime(2020, 5, 20)
        else:
            startTime= datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M")


        if endTime == None:
            endTime = datetime.datetime.today()
        else:
            endTime = datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M")

        results =  self.Logic.storage.getImages(coordinateN,coordinateE, startTime,endTime)

        cherrypy.response.headers['Content-Type'] = 'application/json'

        for entry in results:
            print(type(entry), entry)
            yield json.dumps({"id": str(entry['_id']) , 'time': str(entry["time"]), 'coordinateN': entry["coordinateN"], 'coordinateE':entry["coordinateE"]}).encode()


    GET._cp_config =  {'response.stream' : True}




    def POST(self, coordinateN, coordinateE, image):
        self.Logic.newImage(coordinateN, coordinateE, image)
