from pymongo.mongo_client import MongoClient

uri = None

# Create a new client and connect to the server
client = MongoClient(uri)
print(client)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print(client["shareline-db"].get_collection(name="shareline-db"))
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

