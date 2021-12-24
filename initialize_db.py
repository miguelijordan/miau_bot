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

if __name__ == '__main__':
    #copyRegexs()

    regexs = RegexsPersistence.RegexsPersistence()
    # Fix the csv file.
    with open('miau-regexs.csv', 'r') as file:
        lines = file.readlines()
        new_lines = []
        for l in lines:
            pieces = l.split(',')
            id = pieces[0]
            regex = pieces[-1]
            answer = ",".join(pieces[1:-1])
            regexs.addRegex({'pattern':regex, 'answer':answer})

            new_lines.append(f'{id},"{answer}",{regex}')
        
    # with open('miau-regex-v2.csv', 'w') as file:
    #     file.writelines(new_lines)
