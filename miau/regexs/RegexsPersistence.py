from pymongo import MongoClient     # Python driver for MongoDB
import re                           # Regular expression operations
from miau.constants import constants

class RegexsPersistence():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client[constants.MIAU_DB]
        self.collection = self.db[constants.REGEXS]
        self.regexs = self.__getCompiledRegexs()

    def addRegex(self, regex):
        prog = None
        try:
            prog = re.compile(regex['pattern'], re.IGNORECASE)
        except:
            raise    # To do: raise and send bot message.

        if prog:
            newRegex = dict(regex)
            newRegex['compiledRegex'] = prog
            self.regexs.append(newRegex)

            self.collection.insert_one(regex)   # Acceso a BD


    def deleteRegex(self, regex):
        self.collection.delete_many({'pattern':regex['pattern'], 'answer':regex['answer']})       # Acceso a BD

        elements = list(filter(lambda x : x['pattern'] == regex['pattern'] and x['answer'] == regex['answer'], self.regexs))
        for e in elements:
            self.regexs.remove(e)

    def getRegexs(self):
        return list(self.collection.find().sort('pattern'))   # Acceso a BD

    def getMatchingRegexs(self, text):
        matchings = list(filter(lambda x : re.search(x['compiledRegex'], text), self.regexs))
        return matchings

    def getBestMatchingRegexs(self, text):
        matchings = self.getMatchingRegexs(text)
        bestMatchings = []
        if len(matchings) > 0:
            maxMatching = max(matchings, key=lambda x : len(re.search(x['compiledRegex'], text).group(0)))
            maxLength = len(re.search(maxMatching['compiledRegex'], text).group(0))
            bestMatchings = list(filter(lambda x : len(re.search(x['compiledRegex'], text).group(0)) == maxLength, matchings))
        return bestMatchings

    def __getCompiledRegexs(self):
        regexs = self.getRegexs()
        for r in regexs:
            r['compiledRegex'] = re.compile(r['pattern'], re.IGNORECASE)
        return regexs

    def clearRegexs(self):
        self.collection.drop()
        self.regexs = []
