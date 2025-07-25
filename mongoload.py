from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.binary import Binary
import os

uri = os.getenv("MONGO_URI")

client = MongoClient(uri, server_api=ServerApi('1'))

db = client["ArtisticNails"]
collection = db["Products"]
allOrders = db["Customers"]

products = list(collection.find())
# print(products)
# for product in products:
#     print(product)

def getOrders():
    orders = list(allOrders.find())
    return orders

def getProducts():
    products = list(collection.find({"custom": "No"}))
    return products
