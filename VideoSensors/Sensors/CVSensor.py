from Sensors import Sensor
import cv2

class CVSensor(Sensor):

    stream = None

    def __init__(self, videoSource):
        self.stream = cv2.VideoCapture(videoSource)

    def __del__(self):
        self.stream.release()

    def getFrame(self):
        if not self.stream.isOpened():
            return None

        ret, frame = self.stream.read()

        if ret:
            return frame
        else:
            return None
