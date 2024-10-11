from pymongo import MongoClient

MONGODB_URI = 'mongodb+srv://jameefahim:bigdata@hetionet.q0qji.mongodb.net/?retryWrites=true&w=majority&appName=HetioNet'

client = MongoClient(MONGODB_URI)

for db_name in client.list_database_names():
    print(db_name)

