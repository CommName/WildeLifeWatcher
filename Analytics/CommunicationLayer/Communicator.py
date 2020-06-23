import cv2
import json
import base64
from abc import ABC, abstractmethod
import numpy as np

class Communicator(ABC):

    @abstractmethod
    async def sendMessage(self, analysedData):
        pass

    @abstractmethod
    async def recvMessage(self, msg):
        pass


    def encodeMessageJSON(self, image, imageId):
        _, imdata = cv2.imencode('.JPG', image)
        imageAsString = base64.b64encode(imdata).decode()
        jsonData = json.dumps({"imageId": imageId, "image": imageAsString})
        return jsonData

    def decodeMessageJSON(self, jsonData):
        imageAsString = jsonData["image"]
        jpg_original = base64.b64decode(imageAsString)
        jpg_as_np = np.frombuffer(jpg_original,dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np,flags=1)
        return img, jsonData["imageId"], jsonData["CoordinateN"], jsonData["CoordinateE"]

