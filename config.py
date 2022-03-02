import pymongo
import certifi

mongo_url = "mongodb+srv://FSDI_Greenkey:FSDI@cluster0.awxez.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url, tlsCAFile=certifi.where())

db = client.get_database("Store")