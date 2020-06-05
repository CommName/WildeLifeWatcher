import cv2
import base64
import json

class SensorNotify:

    N = 0
    E = 0
    subscribers = []

    def __init__(self, cordN, cordE):
        self.N = cordN
        self.E = cordE
        self.subscribers = []

    def __del__(self):
        jsonData = json.dumps({ "Type" : "Sensor down"})
        for socket in self.subscribers:
            socket.send(json.encode())


    def subscribe(self, socket):
        self.subscribers.append(socket)

    def unsubsribe(self, socket):
        self.subscribers.remove(socket)

    def notify(self, image):
        _, imdata = cv2.imencode('.JPG', image)
        imageAsString = base64.b64encode(imdata).decode()
        jsonData = json.dumps({"Type": "New sesnor image", "coordinateN" : self.N, "coordinateE" : self.E, "image": imageAsString})
        for socket in self.subscribers:
            socket.send(jsonData.encode())