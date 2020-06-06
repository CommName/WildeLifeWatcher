from datetime import datetime
from time import sleep
import asyncio
from RegistryFiles import ServiceRegistry
import json
import threading

class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)

@Singleton
class Registry(object):

    services = {}
    communicator = None

    def __init__(self):
        self.services = {}
        cleanupthread = threading.Thread(target=self.cleanup)
        cleanupthread.start()



    def cleanup(self):
        while True:
            for key in self.services.keys():
                deleteServices = []
                for service in self.services[key]:
                    if (datetime.now() - service.time).total_seconds() > 10:
                        deleteServices.append(service)

                for service in deleteServices:
                    self.unregistryService(service.serviceName,service.serviceAddress,service.serviceport,service.serviceName)

            sleep(10)


    def registryService(self, serviceName, serviceAddress, servicePort, serverName):
        if not (serviceName in self.services.keys()):
            self.services[serviceName] = []

        for service in self.services[serviceName]:
            if service.serverName == serverName:
                service.serviceAddress = serviceAddress
                service.serviceport = servicePort
                service.time = datetime.now()
                return

        newservice = ServiceRegistry.ServiceRegistry(serviceName, serviceAddress, servicePort, serverName)

        self.services[serviceName].append(newservice)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.communicator.sendMessage("New service "+ serviceName+" server" + newservice.serverName + " address "+ newservice.serviceAddress))


    def unregistryService(self, serviceName, serviceAddress, servicePort, serverName):
        if not serviceName in self.services.keys():
            return

        found = None
        for service in self.services[serviceName]:
            if service.serviceName == serviceName and service.serviceAddress == serviceAddress:
                found = service
                break

        if not found is None:
            self.services[serviceName].remove(service)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.communicator.sendMessage("Removed service "+service.serviceName+" server" + service.serverName + " address "+ service.serviceAddress))


    def getServices(self, serviceName):
        knownservices = []
        if serviceName in self.services.keys():
            for service in self.services[serviceName]:
                knownservices.append(service.dic())
        return json.dumps(knownservices)





