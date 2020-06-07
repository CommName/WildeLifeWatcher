import requests
import json

class ServiceRegistryCache:

    animals = []
    sensors = []
    address = "http://127.0.0.1:8761/"
    parent = None

    def __init__(self, parent):
        self.parent = parent
        self.animals = []
        with open('./RawData/animalList.txt') as fp:
            for line in fp:
                self.animals.append(line)

        self.sensors = {}
        self.reloadSensors()



    def reloadSensors(self):
        s = requests.Session()
        parametars = {"serviceName": "Sensors"}
        r = s.get(self.address, params=parametars)
        if r.status_code >= 200 and r.status_code < 300:
            serviceArray = json.loads(r.text)
            for sensor in self.sensors:
                sensor.Updated = False

            for service in serviceArray:
                if service["ServiceName"] != "Sensors":
                    continue

                if service["ServerName"] in self.sensors:
                        self.sensors[service["ServerName"]].serviceAddress = service["ServiceAddress"]
                        self.sensors[service["ServerName"]].Updated = True
                else:
                    N = 0
                    E = 0
                    try:
                        rs = s.get(service["ServiceAddress"])
                    except requests.exceptions.RequestException as e:  # This is the correct syntax
                        print(e)
                        continue
                    if rs.status_code>= 200 and rs.status_code < 300:
                        print(rs.text)
                        serviceStatus = json.loads(rs.text)
                        N = serviceStatus["CoordinateN"]
                        E = serviceStatus["CoordinateE"]
                        newsensor = SensorData(service["ServerName"], service["ServiceAddress"], N, E)
                        self.sensors[service["ServerName"]] = newsensor

                self.parent.addSensor(service["ServerName"])

            for key in self.sensors:
                if self.sensors[key].Updated == False:
                    self.parent.removeSensor(self.sensors[key].ServerName)
                    self.sensors.pop(key)


    def getUserSensors(self):
        sensors = []
        for key in self.sensors:
            sensors.append(self.sensors[key].userDic())

        return sensors


class SensorData:
    ServerName = ""
    ServiceAddress = ""
    Updated = True
    N = 0
    E = 0

    def __init__(self, ServerName, ServiceAddress, N , E):
        self.ServerName = ServerName
        self.ServiceAddress = ServiceAddress
        self.N = N
        self.E = E
        self.Updated = True

    def userDic(self):
        return {"Name": self.ServerName, "N" : self.N, "E" : self.E}
