from CommunicationLayer import ServiceRegistry
import argparse
import cherrypy
from Commands import CommandContainer

#Main
#arguments
ap = argparse.ArgumentParser()

ap.add_argument('-p', '--port', default="9030", required=False, help='Port on which API runs')
ap.add_argument('-n', '--name', default="Command1", required=False, help='Name of service')
args = vars(ap.parse_args())
args["port"] = int(args["port"])


cherrypy.config.update({'server.socket_port': args["port"]})
cherrypy.config.update({'server.socket_host': '0.0.0.0'})

ServiceRegistry.registry("Command",args["name"], args["port"])


CommandContainerAPI = CommandContainer.CommandContainer()

conf = {
        '/': {
            'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on' : True,
            'tools.response_headers.headers' : [('Content-Type', 'text/plain')]
    }
}
cherrypy.tree.mount(CommandContainerAPI,"/",conf)
cherrypy.engine.start()
cherrypy.engine.block()