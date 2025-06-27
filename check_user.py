from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash
import os
from classes import User

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client['ArtisticNails']
collection = db["Customers"]

def checkUser(email):
    user = collection.find_one({"email": email})
    if user:
        print(user)
        return User(user)  # assume it includes "Password", etc.
    return None

