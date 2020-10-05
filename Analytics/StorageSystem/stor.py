from StorageSystem import MongoStorage
from StorageSystem import Storage

def getStorage(args):
    db = None
    if(args["DataBase"]=="Mongo"):
        print(args["DataBaseName"])
        db = MongoStorage.MongoStorage(args["DataBaseAddress"], dataBaseName=args["DataBaseName"])
    return db