from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.binary import Binary
import os

uri = "mongodb+srv://nevarycolab:1F0J6rXtdrC0zi1X@cluster0.ohuk50d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client["nailArt"]
collection = db["Products"]

products = list(collection.find())
# print(products)
# for product in products:
#     print(product)



def getProducts():
    products = list(collection.find())
    return products
