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