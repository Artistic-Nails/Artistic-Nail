from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash
import os
from classes import User

uri = "mongodb+srv://nevarycolab:1F0J6rXtdrC0zi1X@cluster0.ohuk50d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['nailArt']
collection = db["Customers"]

def checkUser(data):
    email = data.get("email")
    user = collection.find_one({"email": email})
    if user:
        print(user)
        return User(user)  # assume it includes "Password", etc.
    return None

