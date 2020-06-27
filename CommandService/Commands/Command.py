import json
import cherrypy
import requests
from CommunicationLayer import ServiceRegistry

@cherrypy.expose
class Command:

    address = ""

    listOfParametars = []
    typeOfParametars = []

    addressOfActuator = "/"
    listOfParametarsOfActuator = []





    def getServices(self, serviceName):
        ServiceRegistry.getServices(serviceName)


    def castToType(self, value, type):
        if type == "string":
            return  str(value)

        if type == "int":
            return int(value)

        if type == "float":
            return float(value)

        return  value



    def tooString(self):
        respone = "{\n"

        respone += 'Address : "' + self.address + '"\n'

        respone += "Request :  { \n"
        index = 0
        while index < len(self.listOfParametars):
            respone += self.listOfParametars[index] + " " + self.typeOfParametars[index] + "\n"
            index+=1
        respone += "}\n"

        respone += "Sensor query :  { "
        index = 0
        while index < len(self.listOfParametars):
            respone += self.listOfParametarsOfActuator[index] + " " + self.typeOfParametars[index] + "\n"
            index += 1
        respone += "}\n"

        respone += "}\n"

        return respone


    def POST(self,coordinateN, coordinateE, listOfParamtears):
        listOfParamtears = listOfParamtears.split(',')
        coordinateN = float(coordinateN)
        coordinateE = float(coordinateE)
        print(listOfParamtears)
        if len(listOfParamtears) != len(self.listOfParametars):
            #TODO Throw HTTP error
            return

        index = 0;
        query = {}
        while index<len(listOfParamtears):
            query[self.listOfParametarsOfActuator[index]] = self.castToType(listOfParamtears[index], self.typeOfParametars[index])
            index += 1

        serviceArray = self.getServices("Sensors")

        for service in serviceArray:
            try:
                serviceInfo =  requests.get(service["ServiceAddress"])
                serviceInfo = json.loads(serviceInfo.text)
                if serviceInfo["CoordinateN"] ==coordinateN and serviceInfo["CoordinateE"] == coordinateE:
                    print(query)
                    requests.post(service["ServiceAddress"]+self.addressOfActuator, params = query)
                    return
            except requests.exceptions.RequestException as e:
                print(e)
                continue




