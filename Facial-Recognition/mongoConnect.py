import os
import sys
from pymongo import MongoClient
from random import randint
from pprint import pprint


def main(arg1):
    #print(arg1)
    #Step 0: Pass ID from faces-train to current. Filter the collection for ID, then return that doc.
    #Step 1: Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/') #find the proper connection string
    db=client.face_id
    #Data already exists in the db
    collection = db.users
    cursor = collection.find({'NameID':arg1})
    for document in cursor:
        pprint(document)
    return cursor
    
