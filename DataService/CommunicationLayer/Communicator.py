import cv2
import json
import base64
from abc import ABC, abstractmethod
import numpy as np

class Communicator(ABC):



    @abstractmethod
    async def sendMessage(self, image, imageId, CoordinateN, CoordinateE):
        pass

    @abstractmethod
    async def recvMessageFromSensors(self, msg):
        pass

    @abstractmethod
    async def recvRequest(self, msg):
        pass

    def encodeMessageJSON(self, image, imageId, CoordinateN, CoordinateE):
        _, imdata = cv2.imencode('.JPG', image)
        imageAsString = base64.b64encode(imdata).decode()
        jsonData = json.dumps({"imageId": str(imageId), "image": imageAsString, "CoordinateN": CoordinateN, "CoordinateE":CoordinateE})
        return jsonData

    def decodeMessageJSON(self, jsonData):
        imageAsString = jsonData["image"]
        jpg_original = base64.b64decode(imageAsString)
        jpg_as_np = np.frombuffer(jpg_original,dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np,flags=1)
        return img, jsonData["CoordinateN"], jsonData["CoordinateE"]