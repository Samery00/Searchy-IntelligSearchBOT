# import the MongoClient class
from pymongo import MongoClient

# import the Pandas library
import pandas

# these libraries are optional
import json
import time

# build a new client instance of MongoClient
mongo_client = MongoClient('localhost', 27017)

# create new database and collection instance
db = mongo_client.Knowledge_Base
col = db.websites

# start time of script
start_time = time.time()

# make an API call to the MongoDB server
cursor = col.find()
# extract the list of documents from cursor obj
mongo_docs = list(cursor)
print ("total docs:", len(mongo_docs))
# create an empty DataFrame for storing documents
docs = pandas.DataFrame(columns=[])
# iterate over the list of MongoDB dict documents
for num, doc in enumerate(mongo_docs):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pandas.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)
# EXPORT THE MONGODB DOCUMENTS
print ("\nexporting Pandas objects to different file types.")
print ("DataFrame len:", len(docs))
# export the MongoDB documents as a JSON file
docs.to_json("exportdb.json")
print ("\n\ntime elapsed:", time.time()-start_time)
