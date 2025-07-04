from pymongo import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
import os

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["ArtisticNails"]
customers = db["Customers"]

def addUser(username, email, phone, address, cart, size):

    user = {
        "username": username,
        "email": email,
        "phone": phone,
        "address": address,
        "wishlist": [],
        "cart": cart,
        "size": size
    }

    result = customers.insert_one(user)
    user["_id"] = result.inserted_id
    return user