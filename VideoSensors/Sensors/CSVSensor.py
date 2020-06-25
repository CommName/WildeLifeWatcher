from Sensors import Sensor
import csv
import urllib.request
import numpy as np
import cv2

class CSVSensor:

    csvFile = None

    def loadCVSFile(self, file):
        csvfile = open(file, newline='')
        self.csvFile = csv.DictReader(csvfile)

    def getFrame(self):
        try:
            row = next(self.csvFile)
            resp = urllib.request.urlopen(row["url"])
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            return cv2.imdecode(image,cv2.IMREAD_COLOR)
        except StopIteration:
            return None

    def skipFrames(self, numberOfFramesToSkip):
        index = 0
        while index<numberOfFramesToSkip:
            row = next(self.csvFile)
            index +=1


