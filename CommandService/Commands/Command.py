import json
import cherrypy
import requests

@cherrypy.expose
class Command:

    address = ""

    listOfParametars = []
    typeOfParametars = []

    addressOfActuator = "/"
    listOfParametarsOfActuator = []


    serviceRegistryAddress = "http://127.0.0.1:8761/"


    def getServices(self, serviceName):

        s = requests.Session()

        parametars = {"serviceName": serviceName}

        r = s.get(self.serviceRegistryAddress, params=parametars)
        if r.status_code < 200 or r.status_code >= 300:
            return []

        servicesArray = json.loads(r.text)
        if len(servicesArray) == 0:
            return []

        return servicesArray

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
            respone += self.listOfParametars[index] + " " + self.typeOfParametars + "\n"
            index+=1
        respone += "}\n"

        respone += "Sensor query :  { "
        index = 0
        while index < len(self.listOfParametars):
            respone += self.listOfParametarsOfActuator[index] + " " + self.typeOfParametars + "\n"
            index += 1
        respone += "}\n"

        respone += "}\n"

        return respone


    def POST(self,coordinateN, coordianteE, listOfParamtears):

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
            serviceInfo =  requests.get(service["ServiceAddress"])
            serviceInfo = json.loads(serviceInfo.text)
            if serviceInfo["CoordinateN"] ==coordinateN and serviceInfo["CoordinateE"] == coordianteE:
                requests.post(service["ServiceAddress"]+self.address, params = query)
                return




