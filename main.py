
import random
from time import sleep
from pyscript import web, when

s = {
    "won_games": [],
    "highscore": None,
    "num": None,
    "tries": 0
}

def print():
    web.div(text, classes=["output"])

def start_game():
    s["scores"] = []
    s["highscore"] = None
    s["num"] = None
    s["tries"] = 0
    new_round()

def new_round():
    s["num"] = random.randint(1,100)
    s["tries"] = 0

def handle_input(command):
    if command in ("q", "quit", "exit"):
        print("Dein Highscore war: ", s["highscore"])
        print("Deine Scores waren:", ", ".join(s["scores"]))
        exit()
    elif command in ("s", "score", "highscore"):
        print("Dein aktueller Highscore ist:", s["highscore"])
        print("Deine bisherigen Scores sind:", ", ".join(s["scores"]))
    elif command in ("h", "hilfe", "help"):
        print("Verfügbare Abkürzungen:\n  q  =  \"quit\"\n  s  =  \"score\"\n  h  =  \"hilfe\"\n  r  =  reset\n  c  =  \"cheat\"\nWarte was, es gibt cheats?")
    elif command in ("c", "cheat"):
        print("Pssst... Willst du ne Acht kaufen?")
        s["num"] = 8
    elif command in ("r", "reset"):
        print("Das Spiel wird zurückgesetzt", end="", flush=True)
        for i in range(3):
            print(".", end="", flush=True)
            sleep(1)
        print("")
        start_game()
    else:
        global guess
        try:
            guess = int(command)
        except ValueError:
            print("Keine gültige Eingabe!")

def check_guess(guess):
    if guess > s["num"]:
        print("Meine Zahl ist kleiner als", guess)
    elif guess < s["num"]:
        print("Meine Zahl ist größer als", guess)
    else:
        print("Bravo! Du hast die Zahl erraten! Du hast", s["tries"], "Versuche gebraucht.")
        s["scores"].append(str(s["tries"]))
        if s["highscore"] == None:
            print(s["tries"], "ist dein erster Highscore. Kannst du ihn überbieten?")
            s["highscore"] = s["tries"]
        elif s["highscore"] > s["tries"]:
            print("Damit hast du deinen alten Highscore von", s["highscore"], "übertroffen!")
            s["highscore"] = s["tries"]
        else:
            print("Dein Highscore bleibt weiterhin", s["highscore"])
        new_round()



start_game()

@when("click", "#input-button")
def send_guess():
    command_input = web.page["input-field"]
    if not command_input:
        return

    guess = None
    command = input("> ")

    handle_input(command)

    if guess is not None:
        s["tries"] += 1
        check_guess(guess)

@when("keypress", "#input-field")
def enter_guess():
    if event.key == "Enter":
        send_guess()