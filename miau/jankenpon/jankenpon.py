import random       # Generate pseudo-random numbers
import pickle       # Python object serialization
import tabulate     # Pretty-print tabular data in Python

from telegram.emoji import Emoji

# CONSTANTS
RESULTS_FILEPATH = "miau/jankenpon/resources/results.dat"

GUU = Emoji.RAISED_FIST    # rock
PAA = Emoji.RAISED_HAND    # paper
CHOKI = Emoji.VICTORY_HAND  # scissor
JANKEN = [GUU, PAA, CHOKI]
GUUS = [GUU, 'g', 'r', 'rock', 'piedra']
PAAS = [PAA, 'p', 'paper', 'papel']
CHOKIS = [CHOKI, 'c', 's', 'scissor', 'tijera']
WIN = 1
DRAW = 0
LOSE = -1

RESULTS = { (GUU, GUU): DRAW,
            (GUU, PAA): LOSE,
            (GUU, CHOKI): WIN,
            (PAA, GUU): WIN,
            (PAA, PAA): DRAW,
            (PAA, CHOKI): LOSE,
            (CHOKI, GUU): LOSE,
            (CHOKI, PAA): WIN,
            (CHOKI, CHOKI): DRAW }

# game methods
def getResult(choice_playerA, choice_playerB):
    return RESULTS[(choice_playerA, choice_playerB)]

def getMiauChoice():
    return random.choice(JANKEN)


# ranking methods
def compareResults(result):
    return result[0]*100 + result[1]*10 + result[2]*-1

def getRanking(results):
    return sorted(results.items(), key=lambda r: compareResults(r[1]), reverse=True)

def tabulateRanking(ranking):
    return tabulate.tabulate(ranking, headers=["Player", "W  D  L"])

# persistence methods
def saveResults(results):
    with open(RESULTS_FILEPATH, 'wb') as file:
        pickle.dump(results, file)

def loadResults():
    with open(RESULTS_FILEPATH, 'rb') as file:
        results = pickle.load(file)
    return results

def getPlayerChoice(arg):
    arg = arg.lower()
    if arg in GUUS:
        return GUU
    elif arg in PAAS:
        return PAA
    elif arg in CHOKIS:
        return CHOKI
    else:
        return None

def jankenpon(bot, update, args):
    if len(args) == 0:
        players_results = loadResults()
        ranking = getRanking(players_results)
        bot.sendMessage(chat_id=update.message.chat_id, text="Elige entre " + str(GUUS) + ", or " + str(PAAS) + ", or " + str(CHOKIS) +
        #bot.sendMessage(chat_id=update.message.chat_id, text="Choose between (" + GUU  + ", " + PAA + ", " + CHOKI + ")" +
        "\nRANKING:\n" +
        tabulateRanking(ranking)
        )
    elif len(args) > 0:
        player_choice = getPlayerChoice(args[0])
        if player_choice is not None:
            miau_choice = getMiauChoice()
            result = getResult(player_choice, miau_choice)
            player_name = update.message.from_user.first_name
            user_name = update.message.from_user.username

            players_results = loadResults()
            player_res = [0,0,0]
            if player_name in players_results:
                player_res = players_results[player_name]

            if result == 1:
                winner = player_name + " gana!"
                player_res[0] += 1
            elif result == -1:
                winner = "Miau gana!!!"
                player_res[2] += 1
            else:
                winner = "Empate!"
                player_res[1] += 1

            players_results[player_name] = player_res
            saveResults(players_results)

            bot.sendMessage(chat_id=update.message.chat_id, text=player_name + " " + player_choice + " - " + miau_choice + " Miau\n" + winner)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Miauuu???")
