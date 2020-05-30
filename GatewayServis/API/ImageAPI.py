import  cherrypy


@cherrypy.popargs('imageName')
class ImageAPI(object):


    @cherrypy.expose()
    def index(self, imageName):
        return "Your images is "+imageName

