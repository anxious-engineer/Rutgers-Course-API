import pymongo

# TODO : HIDE & MODULARIZE
PASSWORD = "makingausableapi"
uri = "mongodb+srv://admin:" + PASSWORD + "@poc-5vbvd.mongodb.net/test"

def get_client():
    return pymongo.MongoClient(uri)
