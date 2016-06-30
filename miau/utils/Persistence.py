from pymongo import MongoClient
from miau.constants import constants

class Persistence():
    def __init__(self, collection_name):
        self.client = MongoClient()
        self.db = self.client[constants.MIAU_DB]
        self.collection = self.db[collection_name]
        self.data = self.getData()              # list in memory for efficiency

    def getData(self):
        return list(self.collection.find())
        
    def save(self, element):
        self.collection.insert_one(element)
        self.data.append(element)

    def delete(self, element):
        self.collection.delete_one(element)
        if element in self.data:
            self.data.remove(element)

    def deleteAll(self, element):
        self.collection.delete_many(element)
        while element in self.data:
            self.data.remove(element)

    def clearData(self):
        self.collection.drop()
        self.data = []
