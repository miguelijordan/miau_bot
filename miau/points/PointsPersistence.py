from pymongo import MongoClient     # Python driver for MongoDB
from pymongo import ReturnDocument
from miau.constants import constants

class PointsPersistence():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client[constants.MIAU_DB]
        self.collection = self.db[constants.POINTS]
        self.points = self.getPoints()

    def addPoint(self, word):
        doc = self.collection.find_one_and_update({'word':word}, {'$inc': {'points': 1}}, upsert=True, return_document=ReturnDocument.AFTER) # Acceso a BD

        e = list(filter(lambda x : x['word'] == word, self.points))
        if e:
            e[0]['points'] += 1
        else:
            self.points.append(doc)

    def substractPoint(self, word):
        doc = self.collection.find_one_and_update({'word':word}, {'$inc': {'points': -1}}, upsert=True, return_document=ReturnDocument.AFTER) # Acceso a BD

        e = list(filter(lambda x : x['word'] == word, self.points))
        if e:
            e[0]['points'] -= 1
        else:
            self.points.append(doc)

    def getPoints(self):
        return list(self.collection.find().sort('word'))   # Acceso a BD

    def getWordPoints(self, word):
        points = 0
        e = list(filter(lambda x : x['word'] == word, self.points))
        if e:
           points = e[0]['points']
        return points

    def clearPoints(self):
        self.collection.drop()
        self.points = []
