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
            prog = re.compile(regex['pattern'])
            newRegex = dict(regex)
            newRegex['compiledRegex'] = prog
            self.regexs.append(newRegex)

            self.collection.insert_one(regex)   # Acceso a BD
        except:
            pass    # To do: raise and send bot message.

    def deleteRegex(self, regex):
        self.collection.remove(regex)       # Acceso a BD

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
        maxLength = max(matchings, key=lambda x : len(re.search(x['compiledRegex'], text).group(0)))
        bestMatchings = list(filter(lambda x : len(re.search(x['compiledRegex'], text).group(0)) == maxLength))
        return bestMatchings

    def __getCompiledRegexs(self):
        regexs = self.getRegexs()
        for r in regexs:
            r['compiledRegex'] = re.compile(r['pattern'], re.IGNORECASE)
        return regexs

    def clearRegexs(self):
        self.collection.drop()
        self.regexs = []
