import threading
import cv2
import json
import base64
from NotificationRegistry import SensorNotify
from NotificationRegistry import ServicesRegistryCache
import os
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

    sessionSubscribtions = {}



    def __init__(self):
        self.animalSubscription = { }
        self.activeSensors = { }
        self.numberOfSensors = 0
        self.sensorLock = threading.Lock()
        self.sessionSubscribtions = { }
        cur_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        with open(cur_dir+'/RawData/animalList.txt') as fp:
            animals = fp.read().splitlines()
            for animalName in animals:
                self.animalSubscription[animalName] = []
        self.serviceRegistry =  ServicesRegistryCache.ServiceRegistryCache(self)


    def addSessionSubscribtion(self, sessionID, animal):
        if sessionID not in self.sessionSubscribtions:
            self.sessionSubscribtions[sessionID] = []
        self.sessionSubscribtions[sessionID].append(animal)

    def removeSessionSubscribtion(self, sessionID, animal):
        if sessionID not in self.sessionSubscribtions:
            self.sessionSubscribtions[sessionID] = []

        if animal in self.sessionSubscribtions[sessionID]:
            self.sessionSubscribtions[sessionID].remove(animal)

    def getUserSubscription(self, sessionID):
        if sessionID not in self.sessionSubscribtions:
            self.sessionSubscribtions[sessionID] = []
        return self.sessionSubscribtions[sessionID]

    def subscribeForAnimal(self, animalName, socket):
        if animalName in self.animalSubscription:
            self.animalSubscription[animalName].append(socket)

    def unsubscribeFromAnimal(self, animalName, socket):
        if animalName in self.animalSubscription:
            if(socket in self.animalSubscription[animalName]):
                self.animalSubscription[animalName].remove(socket)

    def notifyAnimalSubs(self, animalName, imageName):
        if animalName in self.animalSubscription:
            print(animalName, self.animalSubscription)
            for sensor in self.animalSubscription[animalName]:
                sensor.send(json.dumps({"Type":"New animal", "animal":animalName , "image": imageName}))

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



