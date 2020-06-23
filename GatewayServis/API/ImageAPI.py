import  cherrypy
import requests
import json
from CommunicationLayer import ServiceRegistry

@cherrypy.popargs('imageName')
class ImageAPI(object):

    address = "http://127.0.0.1:8761/"

    @cherrypy.expose()
    def index(self, imageName):
        #Get data centaras

        servicesArray = ServiceRegistry.getServices("Data")

        s = requests.Session()

        for service in servicesArray:
            response  = s.get(service["ServiceAddress"]+"/image/"+imageName,)
            if response.status_code >= 200 and response.status_code < 300:
                cherrypy.response.headers["Content-Type"] = 'image/jpeg'
                return response.content

        raise cherrypy.HTTPError(404, "Your image could not be found in any active service")

