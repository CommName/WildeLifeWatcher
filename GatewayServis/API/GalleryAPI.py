import cherrypy
import json
import requests
class GalleryAPI:

    address = "http://127.0.0.1:8761/"

    @cherrypy.expose
    def GetImages(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'

        s = requests.Session()

        # Get data centaras
        s = requests.Session()
        parametars = {"serviceName": "Data"}

        r = s.get(self.address, params=parametars)
        if r.status_code < 200 or r.status_code >= 300:
            raise cherrypy.HTTPError(503, "Registry service not available")

        servicesArray = json.loads(r.text)
        if len(servicesArray) == 0:
            raise cherrypy.HTTPError(503, "Data services are unavailable at the moment")


        for service in servicesArray:
            r = s.get(service["ServiceAddress"]+"/data", stream=True)
            for line in r.iter_content(1024):
                yield  line

    GetImages._cp_config =  {'response.stream' : True}


    @cherrypy.expose
    def dataSearch(self, coordinateN, coordinateE, startTime, endTime):


        cherrypy.response.headers['Content-Type'] = 'application/json'

        s = requests.Session()

        # Get data centaras
        s = requests.Session()
        parametars = {"serviceName": "Data"}

        r = s.get(self.address, params=parametars)
        if r.status_code < 200 or r.status_code >= 300:
            raise cherrypy.HTTPError(503, "Registry service not available")

        servicesArray = json.loads(r.text)
        if len(servicesArray) == 0:
            raise cherrypy.HTTPError(503, "Data services are unavailable at the moment")

        query = { }
        if coordinateE=="" and  float(coordinateE) >0 :
            query["coordinateE"] =  float(coordinateE)
        if coordinateN=="" and float(coordinateN)>0 :
            query["coordinateN"] = float(coordinateE)

        if startTime != "" :
            query["startTime"] = startTime

        if endTime != "":
            query["endTime"] = endTime

        for service in servicesArray:
            r = s.get(service["ServiceAddress"]+"/data",params=query, stream=True)
            for line in r.iter_content(1024):
                yield  line

    dataSearch._cp_config =  {'response.stream' : True}