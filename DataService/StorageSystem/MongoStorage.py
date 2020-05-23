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
            'time' : time,
            'coordinateN' : coordinateN,
            'coordinateE' : coordinateE
        }
        result = self.table.insert_one(image_data)
        return result.inserted_id

    def getImageNames(self, coordinateN, coordinateE):
        images = self.table.find({'coordinateN' : coordinateN, 'coordinateE': coordinateE})
        return images

    def getImages(self, coordinateN, coordinateE, startTime, endTime):
        query = {
            'coordinateN' : 40.0,
            'coordinateE' : 40.0,
            'time' : {'$gte': startTime, '$lt': endTime}
        }
        print(query)
        results =  self.table.find(query).limit(100)

        return results