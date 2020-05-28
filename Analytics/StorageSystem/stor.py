from StorageSystem import MongoStorage
from StorageSystem import Storage

def getStorage(args):
    db = None
    if(args["DataBase"]=="Mongo"):
        db = MongoStorage.MongoStorage(args["DataBaseAddress"])
    return db