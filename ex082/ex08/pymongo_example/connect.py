
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://userweb9:567234@Cluster0.oaw543f.mongodb.net/?retryWrites=true&w=majority",
    server_api=ServerApi('1')
)

db = client.web9

if __name__ == '__main__':
    results = db.privat.find()
    for result in results:
        print(result)

