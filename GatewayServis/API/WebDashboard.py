import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket
import os
import json
from NotificationRegistry import NotificationRegistry


class WebDashboard:
    indexPage = None
    liveStreamPage = None
    galleryPage = None
    imageDescriptionPage = None
    subscriptionPage = None
    animalList = []
    ws_addr = None

    def __init__(self, address="127.0.0.1:8080"):
        self.ws_addr =  address

        cur_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

        index_path = cur_dir+ "/Public/HTML/index.html"
        self.indexPage = open(index_path, 'r').read()

        liveStream_path = cur_dir+"/Public/HTML/LiveStream.html"
        self.liveStreamPage = open(liveStream_path, 'r').read()

        gallery_path = cur_dir+"/Public/HTML/Gallery.html"
        self.galleryPage = open(gallery_path, 'r').read()

        imageDescription_path = cur_dir+"/Public/HTML/ImageDetails.html"
        self.imageDescriptionPage = open(imageDescription_path, 'r').read()

        subscriptionPage_path = cur_dir+"/Public/HTML/Subscribtions.html"
        self.subscriptionPage = open(subscriptionPage_path, 'r').read()

        self.animalList = list(NotificationRegistry.NotificationRegistry.Instance().animalSubscription.keys())
        self.animalList.append("None")
        self.animalList = json.dumps(self.animalList)



    @cherrypy.expose
    def index(self):
        if "animal" not in cherrypy.session:
            cherrypy.session["animal"] = []
        return self.indexPage % {'ws_addr': self.ws_addr}

    @cherrypy.expose
    def Home(self):
        return self.index()

    @cherrypy.expose
    def Live(self):
        if "animal" not in cherrypy.session:
            cherrypy.session["animal"] = []
        return self.liveStreamPage % {'ws_addr': self.ws_addr}

    @cherrypy.expose
    def ImageDescription(self, imageName):
        if "animal" not in cherrypy.session:
            cherrypy.session["animal"] = []
        return self.imageDescriptionPage % {'ws_addr': self.ws_addr,
                                      'imageName': imageName
                                      }

    @cherrypy.expose
    def Gallery(self):
        if "animal" not in cherrypy.session:
            cherrypy.session["animal"] = []
        return self.galleryPage % { 'ws_addr': self.ws_addr,
                                    'search': "",
                                    "coordinateN": "", "coordinateE": "",
                                    'startTime': "", 'endTime': "",
                                    "animalName" : "", "feeding": "", "notfeeding": "",
                                    'animal_list': self.animalList
                                    }

    @cherrypy.expose
    def GallerySearchData(self, coordinateN,coordinateE, startTime, endTime):
        if "animal" not in cherrypy.session:
            cherrypy.session["animal"] = []
        return self.galleryPage % { 'ws_addr': self.ws_addr, 'search': "dataSearch",
                                    "coordinateN":coordinateN, "coordinateE": coordinateE,
                                    'startTime': startTime, 'endTime' : endTime,
                                    "animalName": "", "feeding": "", "notfeeding": "",
                                    'animal_list': self.animalList
                                    }

    @cherrypy.expose
    def GalleryInformationDataSearch(self, animalName, feeding="False", notfeeding="False"):
        if "animal" not in cherrypy.session:
            cherrypy.session["animal"] = []
        return self.galleryPage % {'ws_addr': self.ws_addr, 'search': "infomrationSearch",
                                   "coordinateN": "", "coordinateE": "",
                                   'startTime': "", 'endTime': "",
                                   "animalName": animalName, "feeding": feeding, "notfeeding": notfeeding,
                                   'animal_list': self.animalList
                                   }

    @cherrypy.expose
    def Subscribitons(self):
        if "animal" not in cherrypy.session:
            cherrypy.session["animal"] = []
        return self.subscriptionPage % {  'ws_addr': self.ws_addr,
                                          'animal_list': json.dumps(list(NotificationRegistry.NotificationRegistry.Instance().animalSubscription.keys())),
                                          'active_subs': json.dumps( NotificationRegistry.NotificationRegistry.Instance().getUserSubscription(cherrypy.session.id))
                                          }


    @cherrypy.expose
    def ws(self):
        handler = cherrypy.request.ws_handler