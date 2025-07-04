from pymongo import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
import os

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["ArtisticNails"]
customers = db["Admins"]

def addAdmin(username, email, password):

    user = {
        "username": username,
        "email": email,
        "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    }

    result = customers.insert_one(user)
    user["_id"] = result.inserted_id
    return user
