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
            try:
                r = s.get(service["ServiceAddress"] + "/info",params=query )
                r.raise_for_status()
                details.append(json.loads(r.text))
                break
            except requests.exceptions.RequestException:
                continue

        servicesArray = ServiceRegistry.getServices("Analytics")
        for service in servicesArray:
            try:
                r = requests.get(service["ServiceAddress"] + "/imageSearch", params=query)
                r.raise_for_status()
                details.append(json.loads(r.text))
            except requests.exceptions.RequestException:
                continue

        return json.dumps(details).encode()


    @cherrypy.expose
    def GetImages(self):

        servicesArray = ServiceRegistry.getServices("Data")
        s = requests.Session()
        for service in servicesArray:
            try:
                r = s.get(service["ServiceAddress"]+"/data", stream=True)
                r.raise_for_status()
                for line in r.iter_content(1024):
                    yield  line
            except requests.exceptions.RequestException:
                continue

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
            try:
                r = s.get(service["ServiceAddress"]+"/data",params=query, stream=True)
                r.raise_for_status()
                for line in r.iter_content(1024):
                    yield  line
            except requests.exceptions.RequestException:
                continue

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
            try:
                r = s.get(service["ServiceAddress"] + "/informationSearch", params=query, stream=True)
                r.raise_for_status()
                for line in r.iter_content(1024):
                    yield line
            except requests.exceptions.RequestException:
                continue

    dataSearch._cp_config = {'response.stream': True}