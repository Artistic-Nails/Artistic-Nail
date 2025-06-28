from pymongo import MongoClient

client = MongoClient("mongodb+srv://artisticnailsbyharman:QLbPCWSz9VHKnO3t@cluster0.mbnwbwo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # or your Mongo URI
db = client["ArtisticNails"]
collection = db["Products"]

# Change all 'pink' colours to 'light pink'
result = collection.update_many(
    {"price": 149.99},
    {"$set": {"price": 299}}
)

print(f"Modified {result.modified_count} documents.")