from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()


client = MongoClient(f"mongodb+srv://{os.environ.get("DB_USER")}:"
                     f"{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}/"
                     f"jan?retryWrites=true&w=majority")

db = client.hradil
 
collection_name = db.odpovede

