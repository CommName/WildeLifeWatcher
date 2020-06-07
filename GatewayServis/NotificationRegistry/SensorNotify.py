import cv2
import base64
import json

class SensorNotify:

    sensorName = ""
    subscribers = []

    def __init__(self,sensorName):
        self.subscribers = []
        self.sensorName = sensorName

    def __del__(self):
        jsonData = json.dumps({ "Type" : "Sensor down"})
        for socket in self.subscribers:
            socket.send(json.encode())


    def subscribe(self, socket):
        self.subscribers.append(socket)

    def unsubsribe(self, socket):
        if socket in self.subscribers:
            self.subscribers.remove(socket)

    def notify(self, image):
        print(self.sensorName, self.subscribers)
        _, imdata = cv2.imencode('.JPG', image)
        imageAsString = base64.b64encode(imdata).decode()
        jsonData = json.dumps({"Type": "New sesnor image", "name" : self.sensorName, "image": imageAsString})
        for socket in self.subscribers:
            socket.send(jsonData.encode())