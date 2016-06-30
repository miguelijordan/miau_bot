from pymongo import MongoClient
from miau.constants import constants

class MongoDBPersistence(Persistence):
    def __init__(self, collection_name):
        self.__client = MongoClient()
        self.__db = self.__client[constants.MIAU_DB]
        self.__collection = self.__db[collection_name]
        self.__data = list(self.__collection.find())    # list in memory for efficiency

    def getData(self):
        return self.__data

    def save(self, element):
        self.__collection.insert_one(element)
        self.__data.append(element)

    def delete(self, element):
        self.__collection.delete_one(element)
        if element in self.data:
            self.__data.remove(element)

    def deleteAll(self, element):
        self.__collection.delete_many(element)
        while element in self.data:
            self.__data.remove(element)

    def clearData(self):
        self.__collection.drop()
        self.__data = []
