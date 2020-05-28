from StorageSystem import Storage
from pymongo import MongoClient
class MongoStorage(Storage.Storage):

    client = None
    imageNameDB = None
    table = None;

    def __init__(self,addressURI='mongodb://localhost:27017', dataBaseName="Analytics", tableName='AnalyticsData'):
        self.client = MongoClient(addressURI)
        self.imageNameDB = self.client["Analytics"]
        self.table = self.imageNameDB.AnalyticsData


    def insertAnalyticData(self, imageName, analyticData):
        image_data = {
            'imageName': imageName,
        }
        for key in analyticData:
            image_data[key] = analyticData[key]

        result = self.table.insert_one(image_data)

        print(result)
        return result.inserted_id

    def getAnalyticData(self, imageName, animalName):
        if (animalName is not None):
            query = {
                'imageName': imageName,
                animalName : {'$gte' : 1}
            }
        else:
            query = {
                'imageName': imageName,
            }
        result = self.table.find(query)

        return result





