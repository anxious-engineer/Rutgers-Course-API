import pymongo
from secrets import mongo

# URI to your mongo client here.
print(mongo.MONGO_URI)
client = pymongo.MongoClient(mongo.MONGO_URI)
db = client.test
coll = db.stuff
coll.insert({"test" : "Hello World!"})
