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
        return self.Logic.communciator.encodeMessageJSON(self.Logic.lastFrame, self.Logic.coordinateN, self.Logic.coordinateE, self.Logic.Name)

    def POST(self,command):
        print(command)
        return
