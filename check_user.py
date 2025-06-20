from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash
import os
from classes import User

uri = "mongodb+srv://artisticnailsbyharman:QLbPCWSz9VHKnO3t@cluster0.mbnwbwo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['ArtisticNails']
collection = db["Customers"]

def checkUser(email):
    user = collection.find_one({"email": email})
    if user:
        print(user)
        return User(user)  # assume it includes "Password", etc.
    return None

