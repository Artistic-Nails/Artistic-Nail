from pymongo import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

uri = "mongodb+srv://artisticnailsbyharman:QLbPCWSz9VHKnO3t@cluster0.mbnwbwo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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

addAdmin("Nevary", "aryanmanchanda@hotmail.com", "123456")