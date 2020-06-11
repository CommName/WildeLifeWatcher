import  cherrypy
import requests
import json

@cherrypy.popargs('imageName')
class ImageAPI(object):

    address = "http://127.0.0.1:8761/"

    @cherrypy.expose()
    def index(self, imageName):
        #Get data centaras
        s = requests.Session()
        parametars = {"serviceName": "Data"}

        r = s.get(self.address, params=parametars)
        if r.status_code < 200 or r.status_code >= 300:
            raise cherrypy.HTTPError(503, "Registry service not available")

        servicesArray = json.loads(r.text)
        if len(servicesArray) == 0:
            raise cherrypy.HTTPError(503, "Data services are unavailable at the moment")

        for service in servicesArray:
            response  = s.get(service["ServiceAddress"]+"/image/"+imageName,)
            if response.status_code >= 200 and response.status_code < 300:
                cherrypy.response.headers["Content-Type"] = 'image/jpeg'
                return response.content

        raise cherrypy.HTTPError(404, "Your image could not be found in any active service")

