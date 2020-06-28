from Commands import Command
import cherrypy

@cherrypy.expose
class CommandContainer:
    activeCommands = { }

    def updateCommands(self, commandName, listOfParametars, typeOfParametars, addressOfActuator, listOfParametarsOfActuator):
        if commandName in self.activeCommands:
            self.activeCommands[commandName].listOfParametars = listOfParametars
            self.activeCommands[commandName].addressOfActuator = addressOfActuator
            self.activeCommands[commandName].typeOfParametars = typeOfParametars
            self.activeCommands[commandName].listOfParametarsOfActuator = listOfParametarsOfActuator

        else:
            command = Command.Command()
            command.address = commandName
            command.listOfParametars = listOfParametars
            command.addressOfActuator = addressOfActuator
            command.typeOfParametars = typeOfParametars
            command.listOfParametarsOfActuator = listOfParametarsOfActuator
            self.activeCommands[commandName] = command
            conf = {
                '/': {
                'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on' : True,
                'tools.response_headers.headers' : [('Content-Type', 'text/plain')]
                }
            }
            cherrypy.tree.mount(command,"/"+commandName,conf)
            cherrypy.engine.stop()
            cherrypy.engine.start()

    def PUT(self, commandName,  listOfParametars, typeOfParametars, addressOfActuator, listOfParametarsOfActuator):
        listOfParametars =  listOfParametars.split(",")
        typeOfParametars = typeOfParametars.split(",")
        print(typeOfParametars)
        listOfParametarsOfActuator = listOfParametarsOfActuator.split(",")
        self.updateCommands(commandName, listOfParametars, typeOfParametars, addressOfActuator, listOfParametarsOfActuator)
        return



    def GET(self):
        response = ""
        for commandName in self.activeCommands:
            response += self.activeCommands[commandName].tooString()

        return response







