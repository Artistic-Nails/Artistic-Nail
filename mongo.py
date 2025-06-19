from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.binary import Binary
import os

uri = "mongodb+srv://nevarycolab:1F0J6rXtdrC0zi1X@cluster0.ohuk50d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

db = client["nailArt"]
collection = db["Products"]


def insert_product(image_path):
    with open(image_path, "rb") as img_file:
        image_binary = Binary(img_file.read())

    product = {
        "shape": "Almond",
        "colour": "Black",
        "design": "Butterfly",
        "custom": "No",
        "price": 149.99,
        "stock_count": 20,
        "image": image_binary
    }

    result = collection.insert_one(product)
    print("Inserted with ID:", result.inserted_id)

# Example usage
insert_product("static/images/black/design6.png")