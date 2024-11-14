from pymongo import MongoClient
from decouple import config
import os

client = MongoClient(f"mongodb+srv://{config("DB_USER")}:"
                     f"{config("DB_PASSWORD")}@{config("DB_HOST")}/"
                     f"jan?retryWrites=true&w=majority"
                     f"&appName={config("APP_NAME")}",
                     authMechanism='MONGODB-CR')

db = client.hradil
 
collection_name = db["odpovede"]

print(client)
print(db)
print(collection_name)
