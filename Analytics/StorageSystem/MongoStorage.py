from StorageSystem import Storage
from pymongo import MongoClient
class MongoStorage(Storage.Storage):

    client = None
    imageNameDB = None
    table = None;

    def __init__(self,addressURI='mongodb://localhost:27017', dataBaseName="AnalyticsVGG16", tableName='AnalyticsData'):
        self.client = MongoClient(addressURI)
        self.imageNameDB = self.client["Analytics"]
        self.table = self.imageNameDB.AnalyticsData


    def insertAnalyticData(self, analyticData):
        result = self.table.insert_one(analyticData)
        return result.inserted_id

    def getAnalyticData(self, imageName):

        query = {
            'imageName': imageName,
        }
        result = self.table.find_one(query)

        return result

    def getImagesWith(self, animalName, feeding):
        query = {

        }
        if animalName is not None:
            query[animalName] = True

        if feeding is not None:
            query["Eating"] = feeding

        result = self.table.find(query).sort('_id',-1)

        return result



