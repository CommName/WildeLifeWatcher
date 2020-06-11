from StorageSystem import Storage
from StorageSystem import MongoStorage

def getDatabase(args):

    if(args["DataBase"]=="Mongo"):
        return MongoStorage.MongoStorage(args["DataBaseAddress"])

    return None