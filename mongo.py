import cloudinary
import cloudinary.uploader
from pymongo import MongoClient
import os

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET')
)
# "mongodb+srv://artisticnailsbyharman:QLbPCWSz9VHKnO3t@cluster0.mbnwbwo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # cloud_name='dbp6sexpx',
    # api_key='855881274985551',
    # api_secret='iPU73Wz1slq9EwnRQHJdAaRznKE'


uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["ArtisticNails"]
collection = db["Products"]

# Function to insert product using a Flask-uploaded image
def insert_product(shape, colour, design, price, image):
    try:
        # Upload directly from FileStorage object
        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result['secure_url']

        # Create product dictionary
        product = {
            "shape": shape.capitalize(),
            "colour": colour.capitalize(),
            "design": design.capitalize(),
            "custom": "No",
            "price": float(price),
            "image": image_url
        }

        result = collection.insert_one(product)
        print(f"✅ Inserted as {result.inserted_id}")
        return True

    except Exception as e:
        print(f"❌ Failed to upload or insert: {e}")
        return False
    
def insert_custom_product(shape, colour, price, design="", image="https://res.cloudinary.com/dbp6sexpx/image/upload/v1750451063/ChatGPT_Image_Jun_21_2025_HTML_CSS_Code_e6qbad.png", instructions=""):
    try:
        # Create product dictionary
        product = {
            "shape": shape.capitalize(),
            "colour": colour.capitalize(),
            "design": design,
            "custom": True,
            "price": price,
            "image": image,
            "instructions": instructions
        }

        result = collection.insert_one(product)
        print(f"✅ Inserted as {result.inserted_id}")
        return result.inserted_id

    except Exception as e:
        print(f"❌ Failed to upload or insert: {e}")
        return False
    

def upload_image(image):
    upload_result = cloudinary.uploader.upload(image)
    image_url = upload_result['secure_url']

    return image_url