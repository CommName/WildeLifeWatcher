from abc import ABC, abstractmethod
import imutils

class DataAnalyser(ABC):

    parent = None

    def analyseImage(self, image):
        pass

    def nextAnalyser(self, image, information):
        if self.parent is not None:
            data = self.parent.analyseImage(image)
            for key in data:
                information[key] = data[key]

        return information



def sliding_window(image, stepSize, windowW,windowH):
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            yield  (x,y, image[y:y+windowH, x:x+windowW])

def pyramid(image, scale, minSize = (30,30)):
    yield  image
    while True:
        w = int(image.shape[1] / scale)
        image = imutils.resize(image,width=w)
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break
        yield image



