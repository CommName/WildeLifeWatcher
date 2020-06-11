from datetime import datetime

class ServiceRegistry:

    serviceName = ""
    serviceAddress = "Localhost"
    serviceport = 8080
    time = datetime.now()
    serverName = ""

    def __init__(self, name, serviceAddress, servicePort, serverName):
        self.serviceName = name
        self.serviceAddress = serviceAddress
        self.serviceport = servicePort
        self.time = datetime.now()
        self.serverName = serverName

    def dic(self):
        return { "ServiceName": self.serviceName, "ServiceAddress" : self.getFullAddress(),
                 "ServerName": self.serverName}

    def getFullAddress(self):
        return self.serviceAddress+":"+str(self.serviceport)
