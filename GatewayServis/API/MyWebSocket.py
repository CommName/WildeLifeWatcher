import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from NotificationRegistry import NotificationRegistry

class WebSocketHandler(WebSocket):

    subscribedSensors = []


    def opened(self):
        return

    def received_message(self, m):
        comand = str(m).split(' ')

        #sensor sensorName
        if(comand[0] == "sensor"):
            for sensor in self.subscribedSensors:
                print(sensor)
                NotificationRegistry.NotificationRegistry.Instance().unsubscribeFromSensor(sensor.sensorName,self)
                self.subscribedSensors.remove(sensor)
            NotificationRegistry.NotificationRegistry.Instance().subscribeForSensor(comand[1], self)

        #unsub sensor sensorName
        elif(comand[0] == "unsub" and comand[1] == "sensor"):
            NotificationRegistry.NotificationRegistry.Instance().unsubscribeFromSensor(comand[2])

        #animal animalName
        elif(comand[0] == "animal"):
            NotificationRegistry.NotificationRegistry.Instance().subscribeForAnimal(comand[1])

        #unsub animal animalName
        elif(comand[0] == "unsub" and comand[1] == "animal"):
            NotificationRegistry.NotificationRegistry.Instance().unsubscribeFromAnimal(comand[2])

        return


    def closed(self, code, reason):
        for sensor in self.subscribedSensors:
            sensor.unsubsribe(self)



    def unsubcribeSensor(self, senosr):
        self.subscribedSensors.remove(senosr)

    def subscribeSensor(self, sensor):
        self.subscribedSensors.append(sensor)