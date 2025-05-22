from pymongo import MongoClient

MONGO_URI = "mongodb+srv://juniorthant30:test1234@mern-cluster.ndkobin.mongodb.net/?retryWrites=true&w=majority&appName=MERN-Cluster"

client = MongoClient(MONGO_URI)

db = client["Litestar"]

products= db["products"]
