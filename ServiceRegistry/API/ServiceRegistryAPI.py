import cherrypy
from RegistryFiles import Registry


@cherrypy.expose
class ServiceRegistryAPI(object):


    def GET(self, serviceName = ""):
        return Registry.Registry.Instance().getServices(serviceName)


    def POST(self, serviceName, serviceAddress, servicePort, serverName):
        Registry.Registry.Instance().registryService(serviceName,serviceAddress,servicePort,serverName)