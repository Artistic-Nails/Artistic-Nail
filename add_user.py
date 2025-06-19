from pymongo import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

# uri = "mongodb+srv://nevarycolab:1F0J6rXtdrC0zi1X@cluster0.ohuk50d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(uri, server_api=ServerApi('1'))
# db = client["nailArt"]
# customers = db["Customers"]

# # Sample customers
# sample_customers = [
#     {
#         "username": "nailqueen01",
#         "email": "nailqueen01@example.com",
#         "phone": "9876543210",
#         "password": bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()),  # Replace with hashed password
#     },
#     {
#         "username": "glamgirl02",
#         "email": "glamgirl02@example.com",
#         "phone": "9876543211",
#         "password": bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()),
#     },
#     {
#         "username": "stylediva03",
#         "email": "stylediva03@example.com",
#         "phone": "9876543212",
#         "password": bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()),
#     }
# ]

pas = bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt())
# print(pas)

print(bcrypt.checkpw("123456".encode('utf-8'), pas))

# # Insert data
# customers.insert_many(sample_customers)
# print("Sample customers inserted!")