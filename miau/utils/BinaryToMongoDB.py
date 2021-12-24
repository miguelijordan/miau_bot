from miau.regexs import RegexsPersistence
import pickle       # Python object serialization

REGEXS_FILEPATH = "miau/regexs/resources/regexs.dat"


def copyRegexs():
    regexsDB = RegexsPersistence.RegexsPersistence()
    regexsDB.clearRegexs()
    with open(REGEXS_FILEPATH, 'rb') as file:
        regexs = pickle.load(file)

    for re in regexs.keys():
        regexsDB.addRegex({'pattern':re, 'answer':regexs[re]})

    print("Done!")
    #for re in regexs:
    #    regexsDB.addRegex({'pattern':regexs})
