from pymongo import MongoClient

client = MongoClient("mongodb+srv://artisticnailsbyharman:QLbPCWSz9VHKnO3t@cluster0.mbnwbwo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # or your Mongo URI
db = client["ArtisticNails"]
collection = db["Products"]

# Change all 'pink' colours to 'light pink'
result = collection.update_many(
    {"colour": "Black"},
    {"$set": {"colour": "Blackout Babe"}}
)

print(f"Modified {result.modified_count} documents.")