from CommunicationLayer import ServiceRegistry
import argparse
import cherrypy
from Commands import CommandContainer
from Commands import Command

#Main
#arguments
ap = argparse.ArgumentParser()

ap.add_argument('-p', '--port', default="9040", required=False, help='Port on which API runs')
ap.add_argument('-n', '--name', default="Command1", required=False, help='Name of service')
ap.add_argument('-r', '--ServiceRegistry', default="http://127.0.0.1:8761/", required=False, help='Address of service registry')
args = vars(ap.parse_args())
args["port"] = int(args["port"])


cherrypy.config.update({'server.socket_port': args["port"]})
cherrypy.config.update({'server.socket_host': '0.0.0.0'})

ServiceRegistry.registry("Command",args["name"], args["port"], args["ServiceRegistry"])


CommandContainerAPI = CommandContainer.CommandContainer()

conf = {
        '/': {
            'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on' : True,
            'tools.response_headers.headers' : [('Content-Type', 'text/plain')]
    }
}



command = Command.Command()
command.address = "command"
command.listOfParametars = ["command"]
command.addressOfActuator = "/"
command.typeOfParametars = ["string"]
command.listOfParametarsOfActuator = ["command"]
CommandContainerAPI.activeCommands["command"] = command
conf = {
    '/': {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on' : True,
        'tools.response_headers.headers' : [('Content-Type', 'text/plain')]
    }
}
cherrypy.tree.mount(command,"/command",conf)


cherrypy.tree.mount(CommandContainerAPI,"/",conf)
cherrypy.engine.start()
cherrypy.engine.block()