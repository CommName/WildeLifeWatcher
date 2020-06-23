import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from NotificationRegistry import NotificationRegistry

class WebSocketHandler(WebSocket):

    subscribedSensors = []
    subscribedAnimals = []
    sessionId = ""

    def opened(self):
        self.sessionId = cherrypy.session.id
        return


    def received_message(self, m):
        comand = str(m).split(' ')

        #sensor sensorName
        if(comand[0] == "sensor"):
            for sensor in self.subscribedSensors:
                NotificationRegistry.NotificationRegistry.Instance().unsubscribeFromSensor(sensor.sensorName,self)
                self.subscribedSensors.remove(sensor)
            sensorName = str(m)
            sensorName = sensorName[sensorName.find(' ')+1:]
            NotificationRegistry.NotificationRegistry.Instance().subscribeForSensor(sensorName, self)

        #unsub sensor sensorName
        elif(comand[0] == "unsub" and comand[1] == "sensor"):
            NotificationRegistry.NotificationRegistry.Instance().unsubscribeFromSensor(comand[2])

        #animal animalName
        elif(comand[0] == "animal"):
            NotificationRegistry.NotificationRegistry.Instance().addSessionSubscribtion( self.sessionId, comand[1])

        #unsub animal animalName
        elif(comand[0] == "unsub" and comand[1] == "animal"):
            NotificationRegistry.NotificationRegistry.Instance().removeSessionSubscribtion( self.sessionId, comand[2])


        #subscribe from cookies/session
        elif(comand[0] == "subscribe" and comand[1]=="animals"):
            for animal in  NotificationRegistry.NotificationRegistry.Instance().getUserSubscription( self.sessionId):
                NotificationRegistry.NotificationRegistry.Instance().subscribeForAnimal(animal, self)
                self.subscribedAnimals.append(animal)
        return


    def closed(self, code, reason):
        for sensor in self.subscribedSensors:
            sensor.unsubsribe(self)

        for animal in self.subscribedAnimals:
            NotificationRegistry.NotificationRegistry.Instance().unsubscribeFromAnimal(animal, self)



    def unsubcribeSensor(self, senosr):
        self.subscribedSensors.remove(senosr)

    def subscribeSensor(self, sensor):
        self.subscribedSensors.append(sensor)