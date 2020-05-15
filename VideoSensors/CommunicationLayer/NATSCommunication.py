import asyncio
import base64
import json
from nats.aio.client import Client as NATS
import cv2
import numpy as np

from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

class NATSCommunication:

    nc = None
    sid = None



    async def closeConnection(self):
        #await self.nc.unsubscribe(self.sid)
        await self.nc.close()

    async def connect(self, address=""):
        self.nc = NATS()
        await self.nc.connect()
        self.sid = await self.nc.subscribe("test", cb=self.recvMessage)

    async def sendMessage(self, image, gpsNCoordinate, gpsYCoordinate):
        _, imdata = cv2.imencode('.JPG', image)
        imageAsString = base64.b64encode(imdata).decode()
        jsonData = json.dumps({"CoordinateN" : gpsNCoordinate, "CoordinateY" : gpsYCoordinate, "image":imageAsString})
        await self.nc.publish("test", jsonData.encode())


    async def recvMessage(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = json.loads(msg.data.decode())


        #await self.nc.publish(reply, b'I can help')




async def run(loop):
    test = NATSCommunication()
    await test.connect()

    testSlika = cv2.imread("test.jpg")
    await test.sendMessage(testSlika,5.0,5.0)

    await asyncio.sleep(5,loop)
    await test.closeConnection()

    cv2.waitKey()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()


    """"" imageAsString = data["image"]
        jpg_original = base64.b64decode(imageAsString)
        jpg_as_np = np.frombuffer(jpg_original,dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np,flags=1)
        cv2.imshow("test2.jpg",img)
    """""