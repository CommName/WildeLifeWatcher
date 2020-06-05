import cherrypy
import cv2
import numpy as np
import base64
import asyncio

@cherrypy.expose
class Gateway(object):

    Logic = None

    def __init__(self, logic):
        print('construct')
        self.Logic = logic

    @cherrypy.tools.accept(media = "text/plain")
    def GET(self):
        return self.Logic.communciator.encodeMessageJSON(self.Logic.lastFrame, self.Logic.coordinateN, self.Logic.coordinateE)

    def POST(self, coordinateN, coordinateE, image):
        jpg_original = base64.b64decode(image)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        self.Logic.coordinateE = coordinateE
        self.Logic.coordinateN = coordinateN
        self.Logic.lastFrame = img
        #await self.Logic.communciator.sendMessage(img,coordinateN,coordinateE)
        return
