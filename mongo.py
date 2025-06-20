import cloudinary
import cloudinary.uploader
from pymongo import MongoClient

# Configure Cloudinary
cloudinary.config(
    cloud_name='dw3qxw3vs',
    api_key='425953968713555',
    api_secret='xj7e2GXtmQa-Yh02abBTxBi7t30'
)

# MongoDB Atlas setup
uri = "mongodb+srv://artisticnailsbyharman:QLbPCWSz9VHKnO3t@cluster0.mbnwbwo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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
            "custom": False,
            "price": float(price),
            "image": image_url
        }

        result = collection.insert_one(product)
        print(f"✅ Inserted as {result.inserted_id}")
        return True

    except Exception as e:
        print(f"❌ Failed to upload or insert: {e}")
        return False