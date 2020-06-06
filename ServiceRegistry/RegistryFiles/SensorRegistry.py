from RegistryFiles import ServiceRegistry

class SensorRegistry(ServiceRegistry.ServiceRegistry):

    coordinateN = 40.0
    coordinateE = 40.0

    def __init__(self, name, serviceAddress, servicePort,serverName, coordinateN, coordinateE):
        super().__init__(name,serviceAddress,servicePort,serverName)
        self.coordinateE = coordinateE
        self.coordinateN = coordinateN