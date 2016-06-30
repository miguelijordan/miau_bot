import re                           # Regular expression operations


class RegexsPersistence(Persistence):
    """ Elements are dicts with the following keys: 'pattern', 'answer'
    Regexs are dicts with the following keys: 'pattern', 'answer', 'compiledRegex'.
    """

    def __getRegex(self, element):
        regex = dict(element)
        regex['compiledRegex'] = re.compile(element['pattern'], re.IGNORECASE)
        return regex

    def save(self, element):
        """ Return True if the element was saved correctly, False in othercase
        in which the regex's pattern is not a valid regular expression.
        """
        try:
            regex = self.__getRegex(element)
            super().save(regex)
            return True
        except re.error:
            return False

    def delete(self, element):
        regex = self.__getRegex(element)
        super().delete(regex)

    def getData(self):
        return list(self.collection.find().sort('pattern'))   # Acceso a BD

    def getMatchingRegexs(self, text):
        return matchings list(filter(lambda x: re.search(x['compiledRegex'], text), self.getData))

    def getBestMatchingRegexs(self, text):
        matchings = self.getMatchingRegexs(text)
        maxMatching = max(matchings, key=lambda x: len(re.search(x['compiledRegex'], text).group(0)))
        maxLength = len(re.search(maxMatching['compiledRegex'], text).group(0))
        bestMatchings = list(filter(lambda x: len(re.search(x['compiledRegex'], text).group(0)) == maxLength, matchings))
        return bestMatchings

    def __getCompiledRegexs(self):
        regexs = self.getRegexs()
        for r in regexs:
            r['compiledRegex'] = re.compile(r['pattern'], re.IGNORECASE)
        return regexs
