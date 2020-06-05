import threading
import cv2
import json
import base64
from NotificationRegistry import SensorNotify

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


    def __init__(self):
        self.animalSubscription = { }
        self.activeSensors = []
        self.numberOfSensors = 0
        self.sensorLock = threading.Lock()

        with open('./RawData/animalList.txt') as fp:
            for line in fp:
                self.animalSubscription[line] = []


    def subscribeForAnimal(self, animalName, socket):
        if animalName in self.animalSubscription.keys():
            self.animalSubscription[animalName].append(socket)

    def unsubscribeFromAnimal(self, animalName, socket):
        if animalName in self.animalSubscription.keys():
            self.animalSubscription[animalName].remove(socket)

    def subscribeForSensor(self, N, E, socket):
        for sensor in self.activeSensors:
            if sensor.N == N and sensor.E == E:
                sensor.subscribe(socket)
                socket.subscribeSensor(sensor)
                return

    def unsubscribeFromSensor(self, sensorId, socket):
        if sensorId < len(self.sensorSubscription):
            self.sensorSubscription[sensorId].remove(socket)

    def addSensor(self, sensorN, sensorE):

        self.sensorLock.acquire()
        for sensor in self.activeSensors:
            if sensorN == sensor.N and sensorE == sensor.E:
                self.sensorLock.release()
                return

        newsensor = SensorNotify.SensorNotify(sensorN, sensorE)
        self.activeSensors.append(newsensor)

        self.sensorLock.release()

    def removeSensor(self, sensorN, sensorE):
        self.sensorLock.acquire()
        found = False
        foundSensor = None
        for sensor in self.activeSensors:
            if sensor.N == sensorN and sensor.E == sensorE:
                found = True
                foundSensor = sensor
                break

        if found:
            self.activeSensors.remove(foundSensor)

        self.sensorLock.release()


    def notifySensor(self, image, sensorN, sensorE):
        for sensor in self.activeSensors:
            if sensor.N == sensorN and sensor.E == sensorE:
                sensor.notify(image)
                return

