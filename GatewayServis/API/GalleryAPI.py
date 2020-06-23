import cherrypy
import json
import requests
from NotificationRegistry import NotificationRegistry
from CommunicationLayer import ServiceRegistry
class GalleryAPI:



    @cherrypy.expose
    def GetImageDetails(self, imageName):

        query  = {
            "imageName": imageName
        }

        s = requests.Session()

        servicesArray = ServiceRegistry.getServices("Data")
        details = []
        for service in servicesArray:
            r = s.get(service["ServiceAddress"] + "/info",params=query )
            details.append(json.loads(r.text))
            break

        servicesArray = ServiceRegistry.getServices("Analytics")
        for service in servicesArray:
            print(service["ServiceAddress"] + "/imageSearch")
            r = requests.get(service["ServiceAddress"] + "/imageSearch", params=query)
            details.append(json.loads(r.text))



        return json.dumps(details).encode()


    @cherrypy.expose
    def GetImages(self):

        servicesArray = ServiceRegistry.getServices("Data")
        s = requests.Session()
        for service in servicesArray:
            print(service["ServiceAddress"]+"/data")
            r = s.get(service["ServiceAddress"]+"/data", stream=True)
            for line in r.iter_content(1024):
                yield  line

    GetImages._cp_config =  {'response.stream' : True}




    @cherrypy.expose
    def dataSearch(self, coordinateN, coordinateE, startTime, endTime):

        servicesArray = ServiceRegistry.getServices("Data")
        s = requests.Session()

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

    @cherrypy.expose
    def informationSearch(self, animalName, feeding, notfeeding):

        servicesArray = ServiceRegistry.getServices("Analytics")
        s = requests.Session()

        query = {
        }

        if animalName in list(NotificationRegistry.NotificationRegistry.Instance().animalSubscription.keys()):
            query['animalName'] = animalName

        if feeding != notfeeding:
            query["feeding"] = feeding

        for service in servicesArray:
            r = s.get(service["ServiceAddress"] + "/informationSearch", params=query, stream=True)
            for line in r.iter_content(1024):
                yield line

    dataSearch._cp_config = {'response.stream': True}