from StorageSystem import Storage
from pymongo import MongoClient
class MongoStorage(Storage.Storage):

    client = None
    imageNameDB = None
    table = None;

    def __init__(self, addressURI='mongodb://localhost:27017', ):
        self.client = MongoClient(addressURI)
        self.imageNameDB = self.client["WildLifeImages"]
        self.table = self.imageNameDB.imageNames


    def insertImage(self, time, coordinateN, coordinateE):
        image_data = {
            'time': time,
            'coordinateN': coordinateN,
            'coordinateE': coordinateE
        }
        result = self.table.insert_one(image_data)
        print(result)
        return result.inserted_id

    def getImageNames(self, coordinateN, coordinateE):
        images = self.table.find({'coordinateN' : coordinateN, 'coordinateE': coordinateE})
        return images

    def getImages(self, coordinateN, coordinateE, startTime, endTime):
        query = {
            "time" : { "$gt" : startTime, "$lt" : endTime}
        }

        if not coordinateN is None:
            query["coordinateN"] = coordinateN
        if not coordinateE is None:
            query["coordinateE"] : coordinateE

        print(query)
        results =  self.table.find(query).sort("time", -1)

        return results