import os
import random
import cloudinary
import cloudinary.uploader
from pymongo import MongoClient

cloudinary.config(
    cloud_name='dw3qxw3vs',
    api_key='425953968713555',
    api_secret='xj7e2GXtmQa-Yh02abBTxBi7t30'
)

# MongoDB Atlas setup
client = MongoClient("mongodb+srv://nevarycolab:1F0J6rXtdrC0zi1X@cluster0.ohuk50d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["nailArt"]
collection = db["Products"]

try:        
    upload_result = cloudinary.uploader.upload("/Users/aryanmanchanda/Projects/Nail-Art/static/images/pretty pink/design6.png")
    image_url = upload_result['secure_url']

            # Generate metadata
    product = {
        "shape": "Almond",
        "colour": "Pink",
        "design": "Flower",
        "custom": "No",
        "price": 149.99,
        "stock_count": 20,
        "image": image_url
    }

            # Insert into MongoDB
    result = collection.insert_one(product)
    print(f"✅ Inserted as {result.inserted_id}")

except Exception as e:
    print(f"❌ Failed to upload: {e}")