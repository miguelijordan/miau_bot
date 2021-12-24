from pymongo import MongoClient     # Python driver for MongoDB
from miau.constants import constants

class WordsChatPersistence():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client[constants.MIAU_DB]
        self.collection = self.db[constants.WORDS_CHAT]
        self.data = self.getData

    def addWord(self, user, word):
        self.collection.find_one_and_update({'word':word, 'user': user}, {'$inc': {'count': 1}}, upsert=True, return_document=ReturnDocument.AFTER)
        
    def getUsers(self):
        return map(lambda x : x['user'], self.collection.find().distinct('user'))

        # users = []
        # for u in self.collection.find().distinct('user'):
        #     users += u['user']
        # return users

    def getWords(self, user):
        return list(self.collection.find({'user':user}))

    def clearData(self):
        self.collection.drop()
        self.regexs = []
