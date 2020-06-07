import threading
import cv2
import json
import base64
from NotificationRegistry import SensorNotify
from NotificationRegistry import ServicesRegistryCache
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
class NotificationRegistry(object):

    animalSubscription = None
    sensorSubscription = None
    sensorLock = None
    activeSensors = None
    serviceRegistry = None


    def __init__(self):
        self.animalSubscription = { }
        self.activeSensors = { }
        self.numberOfSensors = 0
        self.sensorLock = threading.Lock()

        with open('./RawData/animalList.txt') as fp:
            for line in fp:
                self.animalSubscription[line] = []
        self.serviceRegistry =  ServicesRegistryCache.ServiceRegistryCache(self)


    def subscribeForAnimal(self, animalName, socket):
        if animalName in self.animalSubscription.keys():
            self.animalSubscription[animalName].append(socket)

    def unsubscribeFromAnimal(self, animalName, socket):
        if animalName in self.animalSubscription.keys():
            self.animalSubscription[animalName].remove(socket)

    def subscribeForSensor(self, serverName, socket):
        print(serverName)
        if serverName in  self.activeSensors:
            self.activeSensors[serverName].subscribe(socket)
            socket.subscribeSensor(self.activeSensors[serverName])

    def unsubscribeFromSensor(self, serverName, socket):
        if serverName in self.activeSensors:
            self.activeSensors[serverName].unsubsribe(socket)

    def addSensor(self, serverName):

        self.sensorLock.acquire()
        if serverName in self.activeSensors:
            self.sensorLock.release()
            return

        newsensor = SensorNotify.SensorNotify(serverName)
        self.activeSensors[serverName] = newsensor

        self.sensorLock.release()

    def removeSensor(self, serverName):
        self.sensorLock.acquire()

        if serverName in self.activeSensors:
            self.activeSensors.pop(serverName)

        self.sensorLock.release()


    def notifySensor(self, image, sensorName):
        if sensorName in self.activeSensors:
            self.activeSensors[sensorName].notify(image)


